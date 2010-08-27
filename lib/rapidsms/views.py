#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4


from rapidsms.backends.base import get_backend

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.views.decorators.http import require_GET
from django.contrib.auth.views import login as django_login
from django.contrib.auth.views import logout as django_logout


@require_GET
def dashboard(req):
    return render_to_response(
        "dashboard.html",
        context_instance=RequestContext(req))


def login(req, template_name="rapidsms/login.html"):
    return django_login(req, **{"template_name" : template_name})


def logout(req, template_name="rapidsms/loggedout.html"):
    return django_logout(req, **{"template_name" : template_name})


def handle_message(request):
    identity = request.GET.get('identity')
    text = request.GET.get('msg')
    backend = get_backend('bucket')
    msg = backend.message(identity, text)
    router = Router()
    router.incoming(msg)
    return HttpResponse('ok')
    