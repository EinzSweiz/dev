from .models import Email, EmailVerification
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

EMAIL_HOST_USER = settings.EMAIL_HOST_USER

def verify_email(email):
    qs = Email.objects.filter(email=email, active=False)
    return qs.exists()

def get_verification_email_msg(verification_instance):
    if not isinstance(verification_instance, EmailVerification):
        return None
    verify_link = verification_instance.get_link()
    return f'Verify email with following link:\n{verify_link}'

#celery task!
def start_verification_event(email):
    email_obj, created = Email.objects.get_or_create(email=email)
    obj = EmailVerification.objects.create(parent=email_obj, email=email)
    sent = send_verification_email(obj.id)
    return obj, sent

def send_verification_email(verify_obj_id): 
    verify_obj = EmailVerification.objects.get(id=verify_obj_id)
    email = verify_obj.email
    text_msg = get_verification_email_msg(verify_obj)
    subject = 'Verify your email'
    from_user = EMAIL_HOST_USER
    to_user_email = email
    return  send_mail(
        subject=subject,
        message=text_msg,
        from_email=from_user,
        recipient_list= [to_user_email],
        fail_silently=False,
    )


def verify_token(token, max_attempts=5):
    qs = EmailVerification.objects.filter(token=token)
    if not qs.exists() and not qs.count() == 1:
        return False, 'Invalid Token', None
    email_exparied = qs.filter(expired=True)
    if email_exparied.exists():
        return False, 'Token Expired Try again please'
    max_attempts_reached = qs.filter(attempts__gte=max_attempts)
    if max_attempts_reached.exists():
        return False, 'Token Expired, used too many times', None
    obj = qs.first()
    obj.attempts += 1
    obj.last_attempt_at = timezone.now()
    if obj.attempts > max_attempts:
        obj.expired = True
        obj.expired_at = timezone.now
    obj.save()
    email_obj = obj.parent
    return True, 'Welcome', email_obj