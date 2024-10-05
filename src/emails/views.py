from django.shortcuts import render, redirect
from django.http import HttpResponse
from .services import verify_token
from .services import start_verification_event
from .forms import EmailForm
from django.contrib import messages
from django_htmx.http import HttpResponseClientRedirect


def logout_btn_hx_view(request):
    if not request.htmx:
        return redirect('/')
    if request.method == 'POST':
        try:
            del request.session['email_id']
        except Exception as e:
            return messages.error(request, f'{e}')
        email_id_in_session = request.session.get('email_id')
        if not email_id_in_session:
            return HttpResponseClientRedirect('/')
    return render(request, 'emails/hx/logout-btn.html', {})


def email_token_login_view(request):
    if not request.htmx:
        return redirect('home')
    form = EmailForm(request.POST or None)
    email_id_in_session = request.session.get('email_id')
    context = {
        'form': form,
        'message': '',
        'show_form': not email_id_in_session,
    }
    if form.is_valid():
        email_val = form.cleaned_data.get('email')
        obj = start_verification_event(email_val)
        context['form'] = EmailForm()
        messages.success(request, 'Your email have been sent!')
    else:
        messages.error(request, f'{form.errors}')
    return render(request, 'emails/hx/email_form.html', context)

def verify_email_token_view(request, token, *args, **kwargs):
    did_verify, msg, email_obj = verify_token(token=token)
    if not did_verify:
        try:
            del request.session['email_id']
        except:
            pass
        messages.error(request, msg)
        return redirect("/login/")
    messages.success(request, msg)
    request.session['email_id'] = f'{email_obj.id}'
    next_url = request.session.get('next_url') or '/'
    if not next_url.startswith('/'):
        next_url = '/'
    return redirect(next_url)