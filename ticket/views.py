from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, get_object_or_404
from graphql_relay import from_global_id

from ticket.models import Ticket


def group_required(*group_names):
    def in_groups(u):
        if u.is_authenticated:
            if bool(u.groups.filter(name__in=group_names)) or u.is_superuser:
                return True
        return False

    return user_passes_test(in_groups)


@group_required('registration_helper')
def issue(request, global_id):
    _, pk = from_global_id(global_id)
    ticket = get_object_or_404(Ticket, id=pk)
    profile = ticket.owner.profile

    context = {
        'profile': profile,
        'ticket': ticket
    }

    return render(request, 'issue.html', context=context)
