from django.db import models
from django.utils.crypto import get_random_string
from sso.models import User


class Game(models.Model):
    id = models.AutoField(primary_key=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="games")
    title = models.CharField(max_length=64, unique=True)
    description = models.CharField(max_length=256)
    date_created = models.DateField(auto_now=True)
    
    def __str__(self):
        return f"<Game {self.id}: {self.title}>"
    
    def question_count(self):
        return QuestionType1.objects.filter(game_origin=self).count()


class GameSession(models.Model):
    id = models.BigAutoField(primary_key=True)
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name="hosted_games")
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="ongoing", null=True)
    code = models.CharField(max_length=6, primary_key=False, editable=False, unique=True)
    active = models.BooleanField(default=False)
    current_question = models.IntegerField(default=0)
    stillopen = models.BooleanField(default=True)
    finished = models.BooleanField(default=False)
    
    class Meta: verbose_name = "Game Session"
    
    def __str__(self):
        return f"<Gamesession {self.id}, hosted by {self.host}, game id {self.game.id}>"
    
    def save(self, *args, **kwargs):
        if not self.code: self.code = get_random_string(6)
        return super(GameSession, self).save(*args, **kwargs)
    
    def serialize(self):
        return {
            "active": self.active,
            "current_question": self.current_question,
            "stillopen": self.stillopen,
        }
    
    def activate(self, *args, **kwargs):
        self.current_question = 1
        self.active = True
        self.finished = False
        return super(GameSession, self).save(*args, **kwargs)
        
    def deactivate(self, *args, **kwargs):
        self.current_question = 0
        self.active = False
        return super(GameSession, self).save(*args, **kwargs)
        
    def nextquestion(self, *args, **kwargs):
        self.current_question = self.current_question + 1
        self.stillopen = True
        return super(GameSession, self).save(*args, **kwargs)
        
    def closequestion(self, *args, **kwargs):
        self.stillopen = False
        return super(GameSession, self).save(*args, **kwargs)
    
    def status(self):
        if not self.active: return "prep"
        if self.stillopen: return "play"
        elif not self.finished: return "closed"
        else: return "finished"


class QuestionTemplate(models.Model):
    id = models.AutoField(primary_key=True)
    game_origin = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="questions")
    question = models.CharField(max_length=128)
    
    class Meta:
        abstract = True
        order_with_respect_to = "game_origin"
    
    
class QuestionType1(QuestionTemplate):
    choice1 = models.CharField(max_length=64, default="")
    choice2 = models.CharField(max_length=64, default="")
    choice3 = models.CharField(max_length=64, default="", blank=True, null=True)
    choice4 = models.CharField(max_length=64, default="", blank=True, null=True)
    CHOICES = [("1", choice1), ("2", choice2), ("3", choice3), ("4", choice4)]
    answer = models.CharField(max_length=1, choices=CHOICES, default="1")
    
    def serialize(self):
        return {
            "question": self.question,
            "choice1": self.choice1,
            "choice2": self.choice2,
            "choice3": self.choice3,
            "choice4": self.choice4,
        }
        
    def saveedit(self, dict, *args, **kwargs):
        self.question = dict["ques"]
        self.choice1 = dict["opt1"]
        self.choice2 = dict["opt2"]
        self.choice3 = dict["opt3"]
        self.choice4 = dict["opt4"]
        self.answer = dict["ans"]
        return super(QuestionType1, self).save(*args, **kwargs)
        
    def get_answer(self):
        return self.answer #TODO


class UserSession(models.Model):
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    gamesession = models.ForeignKey(GameSession, on_delete=models.CASCADE)
    time_joined = models.DateTimeField(auto_now=True)
    score = models.IntegerField(default=0)
    
    def __str__(self):
        return self.player.username
    

class AnswerPairType1(models.Model):
    CHOICES = [("0", "unanswered"), ("1", "c1"), ("2", "c2"), ("3", "c3"), ("4", "c4")]
    answer = models.CharField(max_length=1, choices=CHOICES)
    question = models.ForeignKey(QuestionType1, on_delete=models.CASCADE)
    usersession = models.ForeignKey(UserSession, on_delete=models.CASCADE, related_name="answers")
    
    class Meta: verbose_name = "Type 1 Answer Pair"
