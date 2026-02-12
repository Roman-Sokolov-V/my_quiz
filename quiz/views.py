from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse, reverse_lazy


from quiz.forms import QuizCreateForm, QuestionCreateForm, AnswerFormSet
from quiz.models import Question, Answer, Quiz, Category

#
# def quiz_create_view(request):
#
#     if request.method == "POST":
#
#         quiz_form = QuizCreateForm(request.POST) # modelForm
#         question_formset = QuestionFormSet(request.POST) # modelformset_factory
#
#
#         if  quiz_form.is_valid() and question_formset.is_valid():
#             quiz = quiz_form.save(commit=False)
#             quiz.author = request.user
#             quiz.save()
#
#             questions = question_formset.save(commit=False)
#             for question in questions:
#                 question.quiz = quiz
#                 question.save()
#                 answer_formset = AnswerFormSet(request.POST, instance=question)
#                 if answer_formset.is_valid():
#                     answer_formset.save()
#             return redirect("quiz:quiz_create")
#
#
#     else:
#         quiz_form = QuizCreateForm()
#         question_formset = QuestionFormSet(queryset=Question.objects.none())
#         answer_formset = AnswerFormSet(queryset=Answer.objects.none())
#
#     return render(
#         request,
#         "quiz/quiz_form.html",
#         {
#             "quiz_form": quiz_form,
#             "question_formset": question_formset,
#             "answer_formset": answer_formset,
#         },
#     )




class QuizCreateView(LoginRequiredMixin, generic.CreateView):
    model = Quiz
    form_class = QuizCreateForm
    #fields = ""name", "description", "categories", "difficulty""

    def get_success_url(self):
        return reverse_lazy("quiz:question_create", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

@login_required
def questions_create(request: HttpRequest, pk) -> HttpResponse:
    quiz = Quiz.objects.get(pk=pk)
    if request.method == "POST":
        question_form = QuestionCreateForm(request.POST)
        if question_form.is_valid():
            question = question_form.save(commit=False)
            question.quiz = quiz
            question.save()

            answer_formset = AnswerFormSet(request.POST, instance=question)
            if answer_formset.is_valid():
                answer_formset.save()
                return redirect("quiz:question_create", pk=pk)
    else:
        question_form = QuestionCreateForm()
        answer_formset = AnswerFormSet(queryset=Answer.objects.none())
        return render(
            request,
            "quiz/question_create.html",
            {
                "question_form": question_form,
                "answer_formset": answer_formset,
                "quiz": quiz,
            }
        )