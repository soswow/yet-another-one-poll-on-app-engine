from appengine_django.models import BaseModel
from google.appengine.ext import db

class Question(BaseModel):
    text = db.StringProperty()
    def __repr__(self):
        return self.text

class Answer(BaseModel):
    text = db.StringProperty()
    question = db.ReferenceProperty(Question, collection_name="answers")
    more_link = db.LinkProperty()

    def __repr__(self):
        return self.text

class Choose(BaseModel):
    question = db.ReferenceProperty(Question)
    answers = db.ListProperty(item_type=db.Key)
    user = db.UserProperty(auto_current_user_add=True)
    when = db.DateTimeProperty(auto_now_add=True)