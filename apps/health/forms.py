import datetime

from django import forms

from apps.health.models import Health


class HealthTrackerForm(forms.ModelForm):
    """
    Form for health tracker
    """
    sleep_start = forms.DateTimeField(initial=datetime.datetime.now)
    sleep_end = forms.DateTimeField(initial=datetime.datetime.now)
    steps = forms.IntegerField()
    water = forms.IntegerField()

    class Meta:
        model = Health
        fields = ('sleep_start', 'sleep_end', 'steps', 'water',)
