from django import forms

from .models import finbook,textstream,category,project,search,searchdetails


class finbookForm(forms.ModelForm):
    class Meta:
        model = finbook
        fields = ('description','clarification','category')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].queryset = City.objects.none()

class desForm(forms.ModelForm):

    class Meta:
        model = finbook
        fields = ('description',)

        widgets = {
            'title': forms.TextInput(attrs={'class': 'textinputclass'}),
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent'}),
        }

class textstreamForm(forms.ModelForm):

    class Meta:
        model = textstream
        fields = ('mytext','impression',)

        widgets = {
            'title': forms.TextInput(attrs={'class': 'textinputclass'}),
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent'}),
        }

class projectForm(forms.ModelForm):

    class Meta:
        model = project
        fields = ('projectname','note',)

        widgets = {
            'title': forms.TextInput(attrs={'class': 'textinputclass'}),
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent'}),
        }

class searchForm(forms.ModelForm):

    class Meta:
        model = search
        fields = ('searchname','note',)

        widgets = {
            'title': forms.TextInput(attrs={'class': 'textinputclass'}),
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent'}),
        }

class searchrunForm(forms.Form):


    word1 = forms.CharField(max_length=100, label='First Kye Word')
    word2 = forms.CharField(max_length=100, label='Second Kye Word')
    maxi = forms.IntegerField()

    
