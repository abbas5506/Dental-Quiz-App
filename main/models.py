from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# This class creates Category of Quiz in django DB
class quizCategory(models.Model):
    title = models.CharField(max_length=100)
    details = models.TextField()
    image = models.ImageField(upload_to='cat_images')

    class Meta:
        verbose_name_plural = 'Quiz Categories'

    def __str__(self):
        return self.title

# This class creates Questions of Quiz in django DB
class quizQuestions(models.Model):
    category = models.ForeignKey(quizCategory, on_delete=models.CASCADE)
    question = models.TextField()
    option_1 = models.CharField(max_length=200)
    option_2 = models.CharField(max_length=200)
    option_3 = models.CharField(max_length=200)
    option_4 = models.CharField(max_length=200)
    difficulty_level = models.CharField(max_length=100)
    time_limit = models.IntegerField()
    right_option = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Quiz Questions'

    def __str__(self):
        return self.question

# This class creates submitted answers of Quiz entered by users in django DB
class userSubmittedAnswers(models.Model):
    question = models.ForeignKey(quizQuestions, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    right_answer = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = 'Users Submitted Answers'

