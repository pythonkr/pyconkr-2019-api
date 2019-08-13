from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from graphql_relay import from_global_id

from ticket.models import Ticket, TicketProduct


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

    if request.method == "POST":
        ticket.set_issue()
        return HttpResponse('')

    additional_message = get_additional_messages(profile)
    tshirtsize = get_tshirt_size(ticket)

    product = get_short_product_name(ticket)

    context = {
        'global_id': global_id,
        'profile': profile,
        'ticket': ticket,
        'product': product,
        'additional_message': additional_message,
        'tshirtsize': tshirtsize,
    }

    return render(request, 'issue.html', context=context)


def get_short_product_name(ticket):
    tutorial_keys = {
        154: '따릉이 데이터 크롤링',
        155: '따릉이 데이터 분석',
        156: 'Tensorflow 2.0',
        157: 'TDD 방식의 웹 개발',
        158: 'Streaming Data Pipeline',
        159: 'Object Detection',
        160: '자연어처리 논문 구현',
        161: '얼굴 인식 알고리즘',
        162: 'JupyterHub in K8s',
        163: 'Django in Docker',
        164: 'LibreOffice with python',
        165: '파이썬 3대장',
        166: '',
        167: 'Music & DeepLearning',
        168: '크롤링으로 첫 코딩 하기',
        169: 'Pytest',
        170: 'DNLP using Scikit-Learn/Keras',
        171: 'Data Science with Python',
        172: 'Django in Beanstalk',
        173: '딥러닝 인공지능 기술',
        174: 'aiohttp로 채팅 웹사이트 만들기',
        175: 'Geopandas',
        176: 'cliff',
        177: 'Python Debugging',
        178: 'GluonNLP',
    }
    if ticket.product.type == TicketProduct.TYPE_TUTORIAL:
        return tutorial_keys[ticket.product.tutorial_set.first().id]
    return ''


def get_tshirt_size(ticket):
    if 'tshirtsize' in ticket.options:
        tshirtsize = ticket.options['tshirtsize']
    else:
        tshirtsize = 'XXXX'
    return tshirtsize


def get_additional_messages(profile):
    additional_keys = {
        'is_patron': '개인후원 버튼을 전달',
        'is_open_reviewer': '오픈리뷰어 버튼을 전달',
        'is_speaker': '발표자 버튼을 전달',
        'is_tutorial_owner': '튜토리얼 진행자 버튼을 전달',
        'is_sprint_owner': '스프린트 진행자 버튼을 전달',
        'has_youngcoder': '영코더 버튼을 전달',
        'has_childcare': '차일드 케어 내용을 안내',
    }
    additional_message = []
    for key, value in additional_keys.items():
        try:
            addition = getattr(profile, key)
            if addition:
                additional_message.append(value)
        except AttributeError:
            pass
    return additional_message
