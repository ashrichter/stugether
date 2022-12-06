import datetime

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from bootstrap_modal_forms.forms import BSModalModelForm
from .models import User, Institution, Subject, Friend, Topic


class CreateUserForm(UserCreationForm):
    """
    Form to take information to do with django base user model.
    """
    institution = forms.ModelChoiceField(label="", queryset=Institution.objects.all(), empty_label="Select institution")
    field_of_study = forms.ModelChoiceField(label="", queryset=Subject.objects.all(), empty_label="Select course")

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',
                  'date_of_birth', 'institution', 'field_of_study',
                  'password1', 'password2', 'type')


class DateInput(forms.DateInput):
    """
    To take date input
    """
    input_type = 'date'


class ChangeUserForm(UserChangeForm):
    """
    Form to take information when editing a user profile.
    """
    username = forms.CharField(max_length=30, help_text='Username')
    email = forms.EmailField(max_length=150, help_text='Email')
    first_name = forms.CharField(max_length=30, help_text='First Name')
    last_name = forms.CharField(max_length=30, help_text='Last Name')
    bio = forms.CharField(max_length=127, help_text='Bio', required=False)
    status = forms.ChoiceField(choices=User.STATUS, required=False)
    date_of_birth = forms.DateField(initial=datetime.date.today)
    institution = forms.ModelChoiceField(queryset=Institution.objects, required=False)
    field_of_study = forms.ModelChoiceField(queryset=Subject.objects, required=False)
    profile_image = forms.ImageField(required=False)
    well_being_visibility = forms.ChoiceField(choices=User.WELL_BEING_VISIBILITY, required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'status',
                  'date_of_birth', 'institution', 'field_of_study', 'profile_image',
                  'well_being_visibility',)
        widgets = {
            'date_of_birth': DateInput(),
        }

    def clean_image(self):
        image = self.cleaned_data['profile_image']
        return image


class FriendForm(forms.ModelForm):
    """
    Form that takes information about friend relation.
    """
    sender = forms.ModelChoiceField(widget=forms.HiddenInput(), queryset=User.objects)
    receiver = forms.ModelChoiceField(widget=forms.HiddenInput(), queryset=User.objects)
    accepted = forms.BooleanField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Friend
        fields = ('sender', 'receiver', 'accepted', )


class TopicForm(BSModalModelForm):
    """
    Form for the adding a topic to the system
    """
    title = forms.CharField(max_length=127)
    description = forms.CharField(max_length=255, required=False)
    type = forms.ChoiceField(choices=Topic.TYPES)

    class Meta:
        model = Topic
        fields = ('title', 'description', 'type', )

