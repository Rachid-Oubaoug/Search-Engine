from django import forms

class SearchForm(forms.Form):
	query = forms.CharField(max_length=20,help_text = None, label='',widget=forms.TextInput(attrs={'size': '100','class': 'form-control'}))
	#message = forms.CharField(widget=forms.Textarea)
	#renvoi = forms.BooleanField(help_text=u"Cochez si vous souhaitez obtenir une copie du mail envoye.", required=False)