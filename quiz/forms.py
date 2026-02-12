from django import forms
from django.forms import modelformset_factory, inlineformset_factory
from quiz.models import Question, Answer, Quiz, Category


class CategoryCreateForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ("name", "description")


def get_category_choices():
    def walk(node, level=0):
        result = []
        result.append((node.id, "—" * level + node.name))
        for child in node.children.all():
            result.extend(walk(child, level + 1))
        return result

    choices = []
    for root in Category.objects.filter(parent__isnull=True):
        choices.extend(walk(root))

    return choices


class QuizCreateForm(forms.ModelForm):
    categories = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Quiz
        fields = ("name", "description", "categories", "difficulty")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["categories"].choices = get_category_choices()

    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit:
            instance.save()
            instance.categories.set(self.cleaned_data["categories"])

        return instance



class QuestionCreateForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ("text",)

# QuestionFormSet = modelformset_factory(
#     Question,
#     fields=("text",),
#     extra=2,
#     max_num=2,
#     validate_max=True,
# )



AnswerFormSet = inlineformset_factory(
    Question,
    Answer,
    fields=("text", "is_correct"),
    extra=2,
    max_num=4,
    validate_max=True,
)
