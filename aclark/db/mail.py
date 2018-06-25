from django.core.mail import send_mail
from django.conf import settings as django_settings


def get_recipients(obj):
    """
    Returns first name and email address
    """
    if not obj:
        return []
    model_name = obj._meta.verbose_name
    if model_name == 'contact':
        return [
            (obj.first_name, obj.email),
        ]
    elif model_name == 'estimate':
        return [(i.first_name, i.email) for i in obj.contacts.all()]
    elif model_name == 'note':
        return [(i.first_name, i.email) for i in obj.contacts.all()]
    elif model_name == 'time':
        return [('Alex', 'aclark@aclark.net')]


def mail_compose(obj, **kwargs):
    """
    Compose message based on object type.
    """
    hostname = kwargs.get('hostname')
    mail_from = kwargs.get('mail_from')
    mail_to = kwargs.get('mail_to')
    # Conditionally create message
    model_name = obj._meta.verbose_name
    if model_name == 'newsletter':
        message = obj.text
        subject = obj.subject
    elif model_name == 'time':
        message = '%s' % obj.get_absolute_url(hostname)
        subject = 'Time entry'
    context = {}
    context['mail_from'] = mail_from
    context['mail_to'] = mail_to
    context['message'] = message
    context['subject'] = subject
    return context


def mail_proc(obj, **kwargs):
    """
    Iterate over recipients, compose message, send message to each recipient.
    """
    request = kwargs.get('request')
    hostname = request.META.get('HTTP_HOST')
    mail_from = django_settings.EMAIL_FROM
    recipients = get_recipients(obj)
    for first_name, email_address in recipients:
        mail_send(**mail_compose(
            obj,
            first_name=first_name,
            hostname=hostname,
            mail_from=mail_from,
            mail_to=email_address,
            request=request))


def mail_send(**kwargs):
    """
    Call send_mail finally.
    """
    mail_from = kwargs.get('mail_from')
    mail_to = kwargs.get('mail_to')
    message = kwargs.get('message')
    subject = kwargs.get('subject')
    send_mail(subject, message, mail_from, (mail_to, ), fail_silently=False)
