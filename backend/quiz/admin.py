from django.contrib import admin
from django.db.models import Count, FloatField, F, ExpressionWrapper
from django.db.models.functions import Round
from unfold.admin import ModelAdmin
from django.db import models
from .models import Question, UserAttempt, UserPerformance

@admin.register(Question)
class QuestionAdmin(ModelAdmin):
    """
    Admin configuration for Question model
    """
    list_display = (
        'id', 
        'text_preview', 
        'correct_answer', 
        'total_attempts', 
        'correct_attempt_rate'
    )
    list_filter = ('correct_answer',)
    search_fields = ('text', 'option_a', 'option_b', 'option_c', 'option_d')
    
    def text_preview(self, obj):
        """
        Display a shortened version of the question text
        """
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    text_preview.short_description = 'Question'
    
    def get_queryset(self, request):
        """
        Annotate queryset with additional performance metrics
        """
        qs = super().get_queryset(request)
        return qs.annotate(
            attempts_count=Count('userattempt'),
            correct_attempts=Count('userattempt', filter=models.Q(userattempt__is_correct=True)),
            attempt_rate=ExpressionWrapper(
                Round(
                    F('correct_attempts') * 100.0 / 
                    models.Case(
                        models.When(attempts_count__gt=0, then=F('attempts_count')),
                        default=models.Value(1),
                        output_field=FloatField()
                    ), 
                    2
                ),
                output_field=FloatField()
            )
        )
    
    def total_attempts(self, obj):
        """
        Display total number of attempts for this question
        """
        return obj.attempts_count
    total_attempts.short_description = 'Total Attempts'
    total_attempts.admin_order_field = 'attempts_count'
    
    def correct_attempt_rate(self, obj):
        """
        Display percentage of correct attempts
        """
        return f"{obj.attempt_rate}%" if hasattr(obj, 'attempt_rate') else "N/A"
    correct_attempt_rate.short_description = 'Correct Rate'
    correct_attempt_rate.admin_order_field = 'attempt_rate'

@admin.register(UserAttempt)
class UserAttemptAdmin(ModelAdmin):
    """
    Admin configuration for UserAttempt model
    """
    list_display = (
        'id', 
        'user', 
        'question_preview', 
        'is_correct', 
        'attempted_at'
    )
    list_filter = (
        'is_correct', 
        ('user', admin.RelatedOnlyFieldListFilter),
        ('question', admin.RelatedOnlyFieldListFilter),
        'attempted_at'
    )
    search_fields = (
        'user__username', 
        'user__email', 
        'question__text'
    )
    
    def question_preview(self, obj):
        """
        Display a shortened version of the question text
        """
        return obj.question.text[:50] + '...' if len(obj.question.text) > 50 else obj.question.text
    question_preview.short_description = 'Question'

@admin.register(UserPerformance)
class UserPerformanceAdmin(ModelAdmin):
    """
    Admin configuration for UserPerformance model
    """
    list_display = (
        'user', 
        'total_questions', 
        'correct_answers', 
        'score_percentage',
        'recent_attempts'
    )
    search_fields = (
        'user__username', 
        'user__email'
    )
    
    def get_queryset(self, request):
        """
        Optimize queryset for performance
        """
        return super().get_queryset(request).select_related('user')
    
    def recent_attempts(self, obj):
        """
        Show recent user attempts
        """
        recent = UserAttempt.objects.filter(user=obj.user).order_by('-attempted_at')[:5]
        return ', '.join([
            f"{'✓' if attempt.is_correct else '✗'} {attempt.question.text[:20]}..." 
            for attempt in recent
        ])
    recent_attempts.short_description = 'Recent Attempts'