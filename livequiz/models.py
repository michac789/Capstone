from django.db import models
from sso.models import User
from django.utils.crypto import get_random_string



# Create your models here.

class Game(models.Model):
    id = models.AutoField(primary_key=True)
    game_id = models.CharField(max_length=6, primary_key=False, editable=False, unique=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="games")
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    time_created = models.DateField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.game_id: self.game_id = get_random_string(6)
        return super(Game, self).save(*args, **kwargs)


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

