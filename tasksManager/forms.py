from django import forms
from authentication.models import Topic, Message


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = [
            "title",
            "description",
            "upload"
        ]


class MessageForm(forms.ModelForm):

    class Meta:
        model = Message
        fields = [
            "title",
            "upload"
        ]

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        self.fields['upload'].required = False


class UpdateTopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = [
            "title",
            "description",
            "upload"
        ]
    def __init__(self, *args, **kwargs):
        super(UpdateTopicForm, self).__init__(*args, **kwargs)
        self.fields['title'].required = False
        self.fields['description'].required = False
        self.fields['upload'].required = False


class ConnectionForm(forms.Form):
    student_id = forms.CharField()
