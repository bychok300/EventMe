from django import forms

from .models import Topic, Comments

# forms.py это формы которые ты видишь в html
# хз на самом деле как это ещё описать, я вроде интуитивно понимаю
# но полностью объяснить не могу


class NewTopicForm(forms.ModelForm):
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 5, 'placeholder': 'What is in your mind?'}
        ),
        max_length=4000,
        help_text='The max length of the text is 4000.'
    )
    # пока так, а то если оно не в обяз,
    # то баг всплывает, вьха не находит картинку
    image = forms.ImageField()

    class Meta:
        model = Topic
        fields = ['subject', 'message', 'image']


class CustomCommentForm(forms.ModelForm):
    body = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 3, 'placeholder': 'Any ideas to comment?'}
        ),
        max_length=4000
    )

    class Meta:
        model = Comments
        fields = ['body']