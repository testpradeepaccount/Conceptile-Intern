from django.db import models
from django.contrib.auth.models import User
import random

class Question(models.Model):
    """
    Model to store quiz questions
    """
    text = models.TextField()
    option_a = models.CharField(max_length=200)
    option_b = models.CharField(max_length=200)
    option_c = models.CharField(max_length=200)
    option_d = models.CharField(max_length=200)
    correct_answer = models.CharField(max_length=1, choices=[
        ('a', 'Option A'),
        ('b', 'Option B'),
        ('c', 'Option C'),
        ('d', 'Option D')
    ])

    def __str__(self):
        return self.text[:50]

class UserAttempt(models.Model):
    """
    Model to track individual user attempts
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)
    attempted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'question')

    def __str__(self):
        return f"{self.user.username} - {self.question.text[:20]}"

class UserPerformance(models.Model):
    """
    Model to track user performance
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_questions = models.IntegerField(default=0)
    correct_answers = models.IntegerField(default=0)
    
    @property
    def score_percentage(self):
        """
        Calculate score percentage
        """
        if self.total_questions == 0:
            return 0
        return round((self.correct_answers / self.total_questions) * 100, 2)

    def update_performance(self, is_correct):
        """
        Update performance metrics
        """
        self.total_questions += 1
        if is_correct:
            self.correct_answers += 1
        self.save()

    def __str__(self):
        return f"{self.user.username}'s Performance"