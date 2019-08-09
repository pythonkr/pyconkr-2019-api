from django.urls import re_path

from ticket.views import issue

urlpatterns = [
    re_path(r'^issue/(?P<global_id>[\w=]+)/', issue, name='ticket_issue'),
]
