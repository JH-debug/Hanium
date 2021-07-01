from django import forms
from .models import TBL_IMG_INFO, TBL_BERT_INFO

class TBL_IMG_INFOFORM(forms.ModelForm):
    class Meta:
        model = TBL_IMG_INFO
        fields = '__all__'

class TBL_BERT_INFOFORM(forms.ModelForm):
    class Meta:
        model = TBL_BERT_INFO
        fields = '__all__'
