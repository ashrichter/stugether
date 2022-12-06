from apps.feed.models import Post, Report, Comment, PostTag
from apps.core.models import User, Topic
from django.utils import timezone
from django import forms
from bootstrap_modal_forms.forms import BSModalModelForm


class ReportForm(BSModalModelForm):
    """
    Form for the reporting system
    """
    post = forms.ModelChoiceField(widget=forms.HiddenInput(), queryset=Post.objects)
    reporter = forms.ModelChoiceField(widget=forms.HiddenInput(), queryset=User.objects)
    date_reported = forms.DateTimeField(widget=forms.HiddenInput(), initial=timezone.now)
    reason = forms.ChoiceField(choices=Report.REASON)
    description = forms.CharField(max_length=127, required=False)
    investigated = forms.BooleanField(widget=forms.HiddenInput(), required=False)
    removed = forms.BooleanField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Report
        fields = ('post', 'reporter', 'date_reported', 'reason', 'description',
                  'investigated', 'removed',)


class CommentForm(forms.ModelForm):
    """
    Form for the commenting system
    """
    content = forms.CharField(widget=forms.Textarea(attrs={'rows': '4', }))

    class Meta:
        model = Comment
        fields = ('content',)


class PostTagForm(forms.ModelForm):
    """
    Form used to tagging topic to a post
    """
    post = forms.ModelChoiceField(widget=forms.HiddenInput(), queryset=Post.objects)
    topic = forms.ModelChoiceField(queryset=Topic.objects)

    class Meta:
        model = PostTag
        fields = ('post', 'topic',)
