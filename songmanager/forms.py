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
    # 
    sm_genre_join = forms.ChoiceField(
        choices=[('', 'and/or'), ('and', 'and'), ('or', 'or')],
        required=False,
        widget=forms.Select(attrs={'id': 'sm-genre-join', 'class': 'form-control'})
    )
    sm_genre_modifier_1 = forms.ChoiceField(
        choices=[('', 'contains/does not contain'), ('contains', 'contains'), ('dncontain', 'does not contain')],
        required=False,
        widget=forms.Select(attrs={'id': 'sm-genre-modifier-1', 'class': 'form-control'})
    )
    sm_genre_modifier_2 = forms.ChoiceField(
        choices=[('', 'all/at least one of'), ('all', 'all option(s) for each song'), ('one', 'one or more of the following options')],
        required=False,
        widget=forms.Select(attrs={'id': 'sm-genre-modifier-2', 'class': 'form-control'})
    )
    sm_genre_options_select = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.none(),
        required=False,
        widget=forms.SelectMultiple(attrs={'id': 'sm-genre-options-select', 'class': 'form-control'})
    )
    # 
    sm_atmosphere_join = forms.ChoiceField(
        choices=[('', 'and/or'), ('and', 'and'), ('or', 'or')],
        required=False,
        widget=forms.Select(attrs={'id': 'sm-atmosphere-join', 'class': 'form-control'})
    )
    sm_atmosphere_modifier_1 = forms.ChoiceField(
        choices=[('', 'contains/does not contain'), ('contains', 'contains'), ('dncontain', 'does not contain')],
        required=False,
        widget=forms.Select(attrs={'id': 'sm-atmosphere-modifier-1', 'class': 'form-control'})
    )
    sm_atmosphere_modifier_2 = forms.ChoiceField(
        choices=[('', 'all/at least one of'), ('all', 'all option(s) for each song'), ('one', 'one or more of the following options')],
        required=False,
        widget=forms.Select(attrs={'id': 'sm-atmosphere-modifier-2', 'class': 'form-control'})
    )
    sm_atmosphere_options_select = forms.ModelMultipleChoiceField(
        queryset=Atmosphere.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={'id': 'sm-atmosphere-options-select', 'class': 'form-control'})
    )
    # 
    sm_emotion_join = forms.ChoiceField(
        choices=[('', 'and/or'), ('and', 'and'), ('or', 'or')],
        required=False,
        widget=forms.Select(attrs={'id': 'sm-emotion-join', 'class': 'form-control'})
    )
    sm_emotion_modifier_1 = forms.ChoiceField(
        choices=[('', 'contains/does not contain'), ('contains', 'contains'), ('dncontain', 'does not contain')],
        required=False,
        widget=forms.Select(attrs={'id': 'sm-emotion-modifier-1', 'class': 'form-control'})
    )
    sm_emotion_modifier_2 = forms.ChoiceField(
        choices=[('', 'all/at least one of'), ('all', 'all option(s) for each song'), ('one', 'one or more of the following options')],
        required=False,
        widget=forms.Select(attrs={'id': 'sm-emotion-modifier-2', 'class': 'form-control'})
    )
    sm_emotion_options_select = forms.ModelMultipleChoiceField(
        queryset=Emotion.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={'id': 'sm-emotion-options-select', 'class': 'form-control'})
    )
    # 
    sm_tag_join = forms.ChoiceField(
        choices=[('', 'and/or'), ('and', 'and'), ('or', 'or')],
        required=False,
        widget=forms.Select(attrs={'id': 'sm-tag-join', 'class': 'form-control'})
    )
    sm_tag_modifier_1 = forms.ChoiceField(
        choices=[('', 'contains/does not contain'), ('contains', 'contains'), ('dncontain', 'does not contain')],
        required=False,
        widget=forms.Select(attrs={'id': 'sm-tag-modifier-1', 'class': 'form-control'})
    )
    sm_tag_modifier_2 = forms.ChoiceField(
        choices=[('', 'all/at least one of'), ('all', 'all option(s) for each song'), ('one', 'one or more of the following options')],
        required=False,
        widget=forms.Select(attrs={'id': 'sm-tag-modifier-2', 'class': 'form-control'})
    )
    sm_tag_options_select = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.none(),
        required=False,
        widget=forms.SelectMultiple(attrs={'id': 'sm-tag-options-select', 'class': 'form-control'})
    )
    
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(CombinedForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['sm_genre_options_select'].queryset = user.get_genres()
            self.fields['sm_tag_options_select'].queryset = user.get_tags()
            
    def clean(self):
        cleaned_data = super().clean()
        
        # Field validation
        # If one selected field requires another in a complete ruleset (e.g. a rating comparison operator and integer representing the rating), this ensures both are in the submitted version of the form        
        rating = cleaned_data.get('sm_rating')
        rating_modifier = cleaned_data.get('sm_rating_modifier')
        rating_energy_join = cleaned_data.get('sm_rating_energy_join')
        energy = cleaned_data.get('sm_energy')
        energy_modifier = cleaned_data.get('sm_energy_modifier')
        
        genre = cleaned_data.get('sm_genre_options_select')
        genre_join = cleaned_data.get('sm_genre_join')
        genre_modifier_1 = cleaned_data.get('sm_genre_modifier_1')
        genre_modifier_2 = cleaned_data.get('sm_genre_modifier_2')
        
        atmosphere = cleaned_data.get('sm_atmosphere_options_select')
        atmosphere_join = cleaned_data.get('sm_atmosphere_join')
        atmosphere_modifier_1 = cleaned_data.get('sm_atmosphere_modifier_1')
        atmosphere_modifier_2 = cleaned_data.get('sm_atmosphere_modifier_2')
        
        emotion = cleaned_data.get('sm_emotion_options_select')
        emotion_join = cleaned_data.get('sm_emotion_join')
        emotion_modifier_1 = cleaned_data.get('sm_emotion_modifier_1')
        emotion_modifier_2 = cleaned_data.get('sm_emotion_modifier_2')
        
        tag = cleaned_data.get('sm_tag_options_select')
        tag_join = cleaned_data.get('sm_tag_join')
        tag_modifier_1 = cleaned_data.get('sm_tag_modifier_1')
        tag_modifier_2 = cleaned_data.get('sm_tag_modifier_2')
        
        if genre or genre_modifier_1 or genre_modifier_2:
            if not genre_modifier_1 or genre_modifier_1 == '' or not genre_modifier_2 or genre_modifier_2 == '' or not genre_join or genre_join == '' or not genre or genre == '':
                self.add_error('sm_genre_modifier_1', 'All genre fields are required if a genre is selected.') 

        if rating or rating_modifier:
            if not rating_modifier or rating_modifier == '' or not rating or rating == '':
                self.add_error('sm_rating', 'All rating fields are required if a rating is selected.') 
            if energy or energy_modifier:
                if not rating_energy_join or rating_energy_join == '':
                    self.add_error('sm_rating', "Selecting 'and' or 'or' is required if both rating and energy are included.") 
        
        if energy or energy_modifier:
            if not energy_modifier or energy_modifier == '' or not energy or energy == '':
                self.add_error('sm_rating', 'All energy fields are required if one energy field is selected.') 

        if atmosphere or atmosphere_modifier_1 or atmosphere_modifier_2:
            if not atmosphere_modifier_1 or atmosphere_modifier_1 == '' or not atmosphere_modifier_2 or atmosphere_modifier_2 == '' or not atmosphere_join or atmosphere_join == '' or not atmosphere or atmosphere == '':
                self.add_error('sm_atmosphere_options_select', 'All atmosphere fields are required if one atmosphere field is selected.')
        
        if emotion or emotion_modifier_1 or emotion_modifier_2:
            if not emotion_modifier_1 or emotion_modifier_1 == '' or not emotion_modifier_2 or emotion_modifier_2 == '' or not emotion_join or emotion_join == '' or not emotion or emotion == '':
                self.add_error('sm_atmosphere_options_select', 'All emotion fields are required if one emotion field is selected.')

        if tag or tag_modifier_1 or tag_modifier_2:
            if not tag_modifier_1 or tag_modifier_1 == '' or not tag_modifier_2 or tag_modifier_2 == '' or not tag_join or tag_join == '' or not tag or tag == '':
                self.add_error('sm_atmosphere_options_select', 'All tag fields are required if one tag field is selected.')

        return cleaned_data