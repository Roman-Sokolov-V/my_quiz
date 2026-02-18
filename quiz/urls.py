from django.urls import path

from quiz.views import QuizCreateView, questions_create, CategoryCreateView


app_name = 'quiz'

urlpatterns = [
    path('create/', QuizCreateView.as_view(), name='quiz-create'),
    path('<int:pk>/question_create/', questions_create, name='question-create'),
    path('category_create/', CategoryCreateView.as_view(), name='category-create'),

    #path('<int:pk>/', QuizDetailView.as_view(), name='quiz_detail'),

]