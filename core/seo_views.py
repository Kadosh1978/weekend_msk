from django.http import HttpResponse
from django.template.loader import render_to_string


def robots_txt(request):
    content = render_to_string("robots.txt", {"request": request})
    return HttpResponse(content, content_type="text/plain; charset=utf-8")