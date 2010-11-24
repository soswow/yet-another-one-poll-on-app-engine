from django.shortcuts import render_to_response, redirect
from django.template.context import RequestContext
from google.appengine.api import users
from forms import PollForm, AnswerForm
from models import Choose, Question, Answer
from django.http import HttpResponseNotAllowed

def main_page(request):
    user = users.get_current_user()
    if not user:
        return redirect(users.create_login_url("/"))
    question = get_question()

    if users.is_current_user_admin():
        post = request.POST
        if post:
            question.text = post["answer_name"]
            question.save()
            return redirect("polls.views.main_page")

    answers = question.answers
    user_choose = Choose.gql("WHERE user = :1", user).get()
    user_answer_keys = []
    if user_choose:
        user_answer_keys = user_choose.answers

    return render_to_response('main.html',
                          {'answers':answers,
                           'user_answer_keys':user_answer_keys,
                           'is_admin':users.is_current_user_admin(),
                           'user': user,
                           'log_out_link':users.create_logout_url("/"),
                           'question':question},
                          context_instance=RequestContext(request))

def save_user_choice(request):
    user = users.get_current_user()
    if not user:
        return redirect(users.create_login_url("/"))
    question = get_question()
    post = request.POST
    if post:
        answer_ids = map(int, post.getlist('chooses'))
        answers = Answer.get_by_id(answer_ids)
        user_choose = Choose.gql("WHERE user = :1", user).get()
        if not user_choose:
            user_choose = Choose(question=question)
        user_choose.answers = [a.key() for a in answers]
        user_choose.save()
        
    return redirect("polls.views.thank_you")

def get_question():
    questions = Question.all()
    if questions.count() == 0:
        new_question = Question(text="Dummy text")
        new_question.save()
    else:
        new_question = questions[0]
    return new_question

def add_new_answer(request):
    _check_for_admin()
    post = request.POST
    if post and users.is_current_user_admin():
        new_answer = post["new_answer"]
        new_link = post["new_link"]
        new_question = get_question()
        answer = Answer()
        answer.text=new_answer
        answer.more_link = new_link
        answer.question=new_question
        answer.save()
    return redirect("polls.views.main_page")

def delete_answer(request, answer_id):
    _check_for_admin()
    answer = _get_answer_by_id(answer_id)
    answer.delete()
    return redirect("polls.views.main_page")

def edit_answer(request, answer_id):
    answer = _get_answer_by_id(answer_id)
    return render_to_response('edit_answer.html',
                              {'answer':answer},
                              context_instance=RequestContext(request))

def save_answer(request):
    post = request.POST
    if post:
        answer = _get_answer_by_id(post["id"])
        answer.text = post["text"]
        answer.more_link = post["more_link"]
        answer.save()
    return redirect("polls.views.main_page")

def _check_for_admin():
    if not users.is_current_user_admin():
        raise HttpResponseNotAllowed("Hacker? Go away, looser!")

def _get_answer_by_id(answer_id):
    answer = Answer.get_by_id(int(answer_id))
    return answer

def thank_you(request):
    return render_to_response('thankyou.html', {}, context_instance=RequestContext(request))
