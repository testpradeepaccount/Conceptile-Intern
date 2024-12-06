from django.urls import path
from .views import SignupView, LoginView, LogoutView, DashboardView, QuizView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', DashboardView.as_view(), name='dashboard'),
    path('quiz/', QuizView.as_view(), name='quiz'),
]
