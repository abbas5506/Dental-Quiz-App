from django.contrib import admin
from .import models

# Register your models here.

# To show quiz category in Django DB
admin.site.register(models.quizCategory)

# To show quiz questions in Django DB
class quizQuestionsAdmin(admin.ModelAdmin):
    list_display = ['question','category','difficulty_level']
admin.site.register(models.quizQuestions, quizQuestionsAdmin)

# To show users submitted answers of quiz in Django DB
class userSubmittedAnswersAdmin(admin.ModelAdmin):
    list_display = ['id','user','question','right_answer']
admin.site.register(models.userSubmittedAnswers, userSubmittedAnswersAdmin)
