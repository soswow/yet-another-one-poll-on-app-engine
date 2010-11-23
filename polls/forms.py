# -*- coding: utf-8 -*-
from google.appengine.ext.db import djangoforms
from django.forms import CheckboxSelectMultiple
from models import Answer, Choose

class AnswerModelChoiceField(djangoforms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s (<a href='%s'>Ссылко</a>)" % (obj.text, obj.link)

class PollForm(djangoforms.ModelForm):
    answers = AnswerModelChoiceField(Answer, Answer.all(), widget=CheckboxSelectMultiple, empty_label=None)

    class Meta:
        model = Choose

    def __init__(self,  *args, **kwargs):
        #self.base_fields['answers'].query = Answer.all()
        #self.base_fields['answers'].widget.choices = self.base_fields['answers'].choices
        super(PollForm, self).__init__(*args, **kwargs)
#        self.fields['answers'].empty_label = None

class AnswerForm(djangoforms.ModelForm):
    text = djangoforms.TextProperty()

    class Meta:
        model = Answer