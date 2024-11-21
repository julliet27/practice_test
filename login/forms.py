from django import forms

class newBOOKForm(forms.Form):
    BOOKname = forms.CharField(label='Book Name', max_length=100)
    BOOKauthor = forms.CharField(label='Author Name',max_length=500)