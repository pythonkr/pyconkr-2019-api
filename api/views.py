from django.shortcuts import render


def robots(request):
    http_host = request.get_host()
    if http_host is not None and http_host.startswith("dev.pycon.kr"):
        return render(request, 'dev-robots.txt', content_type='text/plain')
    return render(request, 'robots.txt', content_type='text/plain')
