from django.db import models
from django.db.models import Q

from config.settings import AUTH_USER_MODEL


class Category(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
    )
    class Meta:
        verbose_name_plural = "Categories"
        constraints = [
            models.UniqueConstraint(fields=["name", "parent"], name="unique_parent_children"),
            models.UniqueConstraint(
                fields=["name"], condition=Q(parent__isnull=True), name="unique_root_category"
            ),
        ]

    def __str__(self):
        return self.name

class Question(models.Model):
    text = models.TextField()
    quiz = models.ForeignKey("Quiz", on_delete=models.CASCADE, related_name="questions")

class Answer(models.Model):
    text = models.TextField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    is_correct = models.BooleanField(default=False)

DIFFICULTY_CHOICES = (
    ("easy", "Easy"),
    ("medium", "Medium"),
    ("hard", "Hard"),
)

RATING_CHOICES = (
    (1, "Bad"),
    (2, "Not bad"),
    (3, "Good"),
    (4, "Perfect"),
    (5, "Excellent")
)
class Quiz(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(blank=True, null=True)
    categories = models.ManyToManyField(Category, blank=True, related_name="quizzes")
    difficulty = models.CharField(max_length=250, choices=DIFFICULTY_CHOICES, null=True, blank=True)
    author = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="quizzes")
    created = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(choices=RATING_CHOICES, null=True, blank=True)


class Result(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="results")
    student = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    points = models.FloatField(default=0, null=True, blank=True)
    used_time = models.IntegerField(null=True, blank=True)
    date = models.DateField(auto_now=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["quiz", "student"], name="unique_result_quiz"
            )
        ]


class Feedback(models.Model):
    message = models.TextField()
    author = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="feedbacks")
    created = models.DateTimeField(auto_now_add=True)
