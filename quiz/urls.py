from django.urls import path

from quiz.models import Question
from quiz.views import QuizCreateView, questions_create


app_name = 'quiz'

urlpatterns = [
    path('create/', QuizCreateView.as_view(), name='quiz_create'),
    path('<int:pk>/question_create/', questions_create, name='question_create'),
    #path('<int:pk>/', QuizDetailView.as_view(), name='quiz_detail'),

]