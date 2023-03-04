from django.http import HttpResponseNotFound
from django.shortcuts import redirect, get_object_or_404
import requests
from home.models import HomePage, Contact
import os


def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")


        r = requests.post('https://www.google.com/recaptcha/api/siteverify',
                        data={'response': request.POST.get("g-recaptcha-response"),
                                'secret': os.environ.get("RECHAPTA_SECRET")})

        data = r.json()
        if data["success"]:
            Contact.objects.create(name=name, email=email, message=message)

        page = get_object_or_404(HomePage, slug="contact-success")
        return redirect(page.get_url())

    return HttpResponseNotFound()
