from django.contrib import admin
from .models import Game, GameSession, QuestionType1, AnswerPairType1, UserSession

# Register your models here.
class GameAdmin(admin.ModelAdmin):
    list_display = ("__str__", "creator")
    
class GameSessionAdmin(admin.ModelAdmin):
    list_display = ("__str__", "code", "active", "current_question", "stillopen")


admin.site.register(Game, GameAdmin)
admin.site.register(GameSession, GameSessionAdmin)
admin.site.register(QuestionType1)
admin.site.register(AnswerPairType1)
admin.site.register(UserSession)
