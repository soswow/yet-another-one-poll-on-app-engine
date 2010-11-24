from django.conf.urls.defaults import *

urlpatterns = patterns('polls.views',
    (r'^$', 'main_page'),
    (r'^add_answer$','add_new_answer'),
    (r'^delete_answer/(\d*)$','delete_answer'),
    (r'^edit_answer/(\d*)$','edit_answer'),
    (r'^save_answer$','save_answer'),
    (r'^save_user_choice$','save_user_choice'),
    (r'^thank_you$','thank_you'),
    (r'^statistics$','statistics')
)