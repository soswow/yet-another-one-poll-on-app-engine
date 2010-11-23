import unittest

from models import *
from google.appengine.api.users import User
#from django.test import Client
import models

class MainTest(unittest.TestCase):
    def setUp(self):
        question = Question()
        question.text = "Some Test"
        question.save()

        answer = Answer()
        answer.question = question.key()
        answer.text = "Some Answer"
        answer.save()

        answer2 = Answer()
        answer2.question = question
        answer2.text = "Some Other Answer"
        answer2.save()

        self.user = User("hoho@gmail.com")
        choose = Choose()
        choose.question = question
        choose.answers = [answer.key(), answer2.key()]
        choose.user = self.user
        choose.save()

    def testModel(self):
        gqlQuery = Choose.gql("WHERE user = :1", self.user)
        num = gqlQuery.count()
        self.assertEqual(1, num)
        choose = gqlQuery.get()
        self.assert_(choose)
        self.assertEqual(2, len(choose.answers))
        answers = Answer.get(choose.answers)
        self.assertEqual(2, len(answers))
        self.assertEqual("Some Answer", answers[0].text)


