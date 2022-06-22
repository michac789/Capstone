from django.contrib import admin
from .models import Game, GameSession, QuestionType1, AnswerPairType1

# Register your models here.
class GameAdmin(admin.ModelAdmin):
    list_display = ("__str__", "creator")
    
class GameSessionAdmin(admin.ModelAdmin):
    list_display = ("__str__", "active", "current_question", "stillopen")


admin.site.register(Game, GameAdmin)
admin.site.register(GameSession, GameSessionAdmin)
admin.site.register(QuestionType1)
admin.site.register(AnswerPairType1)
