from . import models
from django.forms import ModelForm


class CreateTodoForm(ModelForm):
    class Meta:
        model = models.TodoItem
        fields = ["title"]
