from django.urls import path

from ticket.views import issue

urlpatterns = [
    path('issue/<slug:global_id>/', issue, name='ticket_issue'),
]
