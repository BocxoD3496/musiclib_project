from django import forms
from .models import Album

class AlbumForm(forms.ModelForm):
    export_format = forms.ChoiceField(choices=(('json','JSON'),('xml','XML')), initial='json')

    class Meta:
        model = Album
        fields = ['title','artist','year','genre','tracks']

    def clean_year(self):
        year = self.cleaned_data['year']
        if year < 1800 or year > 2100:
            raise forms.ValidationError('Год должен быть в диапазоне 1800–2100')
        return year

    def clean_tracks(self):
        tracks = self.cleaned_data['tracks']
        if tracks < 0 or tracks > 200:
            raise forms.ValidationError('Кол-во треков должно быть разумным (0–200)')
        return tracks
