from django.shortcuts import render
from emails.forms import EmailForm
from django.contrib import messages
from emails.models import Email, EmailVerification
from emails.services import start_verification_event


def login_view(request):
    return render(request, 'auth/login.html', {})


def home(request):
    form = EmailForm(request.POST or None)
    context = {
        'form': form,
        'message': ''
    }
    if form.is_valid():
        email_val = form.cleaned_data.get('email')
        # obj = form.save()
        obj = start_verification_event(email=email_val)
        print(obj)
        context['form'] = EmailForm()
        messages.success(request, 'Your email have been sent!')
    else:
        messages.error(request, f'{form.errors}')
    print('email_id', request.session.get('email'))
    return render(request, 'cfehome/home.html', context)