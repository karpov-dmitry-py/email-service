from django.forms import ModelForm
from django.forms import Textarea

from models import Topic
from models import Customer
from models import NewsLetter


# noinspection PyArgumentList
class TopicForm(ModelForm):
    class Meta:
        model = Topic
        fields = ['title', 'desc']
        widgets = {
            'desc': Textarea(attrs={'cols': 50, 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super(TopicForm, self).__init__(*args, **kwargs)
        for field_name in self.fields.keys():
            self.fields[field_name].widget.attrs.update({
                'class': 'form-control',
                'placeholder': 'Add {}'.format(field_name),
            })


# noinspection PyArgumentList
class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'topics']

    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)
        for field_name in self.fields.keys():
            self.fields[field_name].widget.attrs.update({
                'class': 'form-control',
                'placeholder': 'Add {}'.format(field_name),
            })


# noinspection PyArgumentList
class NewsletterForm(ModelForm):
    class Meta:
        model = NewsLetter
        fields = ['title', 'topic', 'body', 'run_immediately']
        widgets = {
            'body': Textarea(attrs={'cols': 50, 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super(NewsletterForm, self).__init__(*args, **kwargs)
        exclude_fields = ('run_immediately',)
        for field_name in self.fields.keys():
            if field_name not in exclude_fields:
                self.fields[field_name].widget.attrs.update({
                    'class': 'form-control',
                    'placeholder': 'Add {}'.format(field_name),
                })
