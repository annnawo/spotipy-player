from django import forms
from django.core.exceptions import ValidationError
from .models import *

# class SmartPlaylistRulesForm(forms.ModelForm):
#     sm_rating_modifier = forms.ChoiceField(choices=[('', '<=/=>'), ('lt', 'is less than'), ('lteq', 'is less than or equal to'), ('eq', 'is equal to'), ('gteq', 'is greater than or equal to'), ('gt', 'is greater than')], required=False)
#     sm_rating = forms.IntegerField(min_value=1, max_value=5, required=False)
#     sm_rating_energy_join = forms.ChoiceField(choices=[('', 'and/or'), ('and', 'and'), ('or', 'or')], required=False)
#     sm_energy_modifier = forms.ChoiceField(choices=[('', '<=/=>'), ('lt', 'is less than'), ('lteq', 'is less than or equal to'), ('eq', 'is equal to'), ('gteq', 'is greater than or equal to'), ('gt', 'is greater than')], required=False)
#     sm_energy = forms.IntegerField(min_value=0, max_value=100, required=False)
#     sm_genre_join = forms.ChoiceField(choices=[('', 'and/or'), ('and', 'and'), ('or', 'or')], required=False)
#     sm_genre_modifier_1 = forms.ChoiceField(choices=[('', '--contains/does not contain--'), ('contains', 'contains'), ('dncontain', 'does not contain')], required=False)
#     sm_genre_modifier_2 = forms.ChoiceField(choices=[('', '--all/at least one of--'), ('all', 'all option(s) for each song'), ('one', 'one or more of the following options')], required=False)
#     sm_genre_options_select = forms.ModelMultipleChoiceField(queryset=Genre.objects.all(), required=False)
#     # Similarly define fields for atmosphere, emotion, and tags

#     class Meta:
#         model = SmartPlaylistRules
#         fields = ['sm_rating_modifier', 'sm_rating', 'sm_rating_energy_join', 'sm_energy_modifier', 'sm_energy', 'sm_genre_join', 'sm_genre_modifier_1', 'sm_genre_modifier_2', 'sm_genre_options_select']

#     def clean(self):
#         cleaned_data = super().clean()
#         genre_contain_choice = cleaned_data.get('genre_contain_choice')
#         print(genre_contain_choice)
#         genre_options_choice = cleaned_data.get('genre_options_choice')
#         genres = cleaned_data.get('genres')
        
#         if genres and (not genre_contain_choice or not genre_options_choice):
#             raise ValidationError({
#                 'genre_contain_choice': 'This field is required if genres are selected.',
#                 'genre_options_choice': 'This field is required if genres are selected.'
#             })
        
        
#         return cleaned_data

class CombinedForm(forms.Form):
    # Playlist fields
    sm_playlist_title = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'id': 'sm-playlist-title',
            'class': 'form-control',
            'placeholder': 'Enter a Playlist Name'
        })
    )
    # SmartPlaylistRules fields
    sm_rating_modifier = forms.ChoiceField(
        choices=[('', '<=/=>'), ('lt', 'is less than'), ('lteq', 'is less than or equal to'), ('eq', 'is equal to'), ('gteq', 'is greater than or equal to'), ('gt', 'is greater than')],
        required=False,
        widget=forms.Select(attrs={'id': 'sm-rating-modifier', 'class': 'form-control'})
    )
    sm_rating = forms.IntegerField(
        min_value=1,
        max_value=5,
        required=False,
        widget=forms.NumberInput(attrs={'id': 'sm-rating', 'class': 'form-control'})
    )
    sm_rating_energy_join = forms.ChoiceField(
        choices=[('', 'and/or'), ('and', 'and'), ('or', 'or')],
        required=False,
        widget=forms.Select(attrs={'id': 'sm-rating-energy-join', 'class': 'form-control'})
    )
    sm_energy_modifier = forms.ChoiceField(
        choices=[('', '<=/=>'), ('lt', 'is less than'), ('lteq', 'is less than or equal to'), ('eq', 'is equal to'), ('gteq', 'is greater than or equal to'), ('gt', 'is greater than')],
        required=False,
        widget=forms.Select(attrs={'id': 'sm-energy-modifier', 'class': 'form-control'})
    )
    sm_energy = forms.IntegerField(
        min_value=0,
        max_value=100,
        required=False,
        widget=forms.NumberInput(attrs={'id': 'sm-energy', 'class': 'form-control'})
    )
    sm_genre_join = forms.ChoiceField(
        choices=[('', 'and/or'), ('and', 'and'), ('or', 'or')],
        required=False,
        widget=forms.Select(attrs={'id': 'sm-genre-join', 'class': 'form-control'})
    )
    sm_genre_modifier_1 = forms.ChoiceField(
        choices=[('', '--contains/does not contain--'), ('contains', 'contains'), ('dncontain', 'does not contain')],
        required=False,
        widget=forms.Select(attrs={'id': 'sm-genre-modifier-1', 'class': 'form-control'})
    )
    sm_genre_modifier_2 = forms.ChoiceField(
        choices=[('', '--all/at least one of--'), ('all', 'all option(s) for each song'), ('one', 'one or more of the following options')],
        required=False,
        widget=forms.Select(attrs={'id': 'sm-genre-modifier-2', 'class': 'form-control'})
    )
    sm_genre_options_select = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.none(),
        required=False,
        widget=forms.SelectMultiple(attrs={'id': 'sm-genre-options-select', 'class': 'form-control'})
    )

    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(CombinedForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['sm_genre_options_select'].queryset = user.get_genres()