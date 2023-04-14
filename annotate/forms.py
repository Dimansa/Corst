from django.forms import ModelForm
from .models import Document


class Text(ModelForm):
    class Meta:
        model = Document
        fields = '__all__'


