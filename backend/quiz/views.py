from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.models import User

from .models import Question, UserAttempt, UserPerformance
from .forms import UserSignupForm, UserLoginForm
import random

class SignupView(View):
    def get(self, request):
        form = UserSignupForm()
        return render(request, 'signup.html', {'form': form})
    
    def post(self, request):
        form = UserSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserPerformance.objects.create(user=user)
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('dashboard')
        return render(request, 'signup.html', {'form': form})

class LoginView(View):
    def get(self, request):
        form = UserLoginForm()
        return render(request, 'login.html', {'form': form})
    
    def post(self, request):
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('dashboard')
        messages.error(request, 'Invalid username or password')
        return render(request, 'login.html', {'form': form})

class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.info(request, 'You have been logged out.')
        return redirect('login')

class DashboardView(LoginRequiredMixin, View):
    def get(self, request):
        """
        Render dashboard with user performance and attempted questions
        """
        performance, created = UserPerformance.objects.get_or_create(user=request.user)
        
        attempted_questions = UserAttempt.objects.filter(user=request.user).select_related('question')
        
        context = {
            'total_questions': performance.total_questions,
            'correct_answers': performance.correct_answers,
            'score_percentage': performance.score_percentage,
            'attempted_questions': attempted_questions
        }
        return render(request, 'dashboard.html', context)

class QuizView(LoginRequiredMixin, View):
    def get(self, request):
        """
        Render a random quiz question
        """
        attempted_question_ids = UserAttempt.objects.filter(user=request.user).values_list('question_id', flat=True)
        questions = Question.objects.exclude(id__in=attempted_question_ids)
        
        if not questions:
            messages.info(request, 'You have attempted all available questions!')
            return redirect('dashboard')
        
        question = random.choice(questions)
        
        context = {
            'question': question,
            'options': [
                {'label': 'A', 'text': question.option_a},
                {'label': 'B', 'text': question.option_b},
                {'label': 'C', 'text': question.option_c},
                {'label': 'D', 'text': question.option_d}
            ]
        }
        return render(request, 'quiz.html', context)
    
    def post(self, request):
        """
        Process quiz answer submission
        """
        question_id = request.POST.get('question_id')
        user_answer = request.POST.get('answer')
        
        try:
            question = Question.objects.get(pk=question_id)
            
            is_correct = (user_answer == question.correct_answer)
            
            UserAttempt.objects.create(
                user=request.user,
                question=question,
                is_correct=is_correct
            )
            
            performance, created = UserPerformance.objects.get_or_create(user=request.user)
            performance.update_performance(is_correct)
            
            context = {
                'question': question,
                'user_answer': user_answer,
                'is_correct': is_correct
            }
            
            return render(request, 'result.html', context)
        
        except Question.DoesNotExist:
            return redirect('dashboard')