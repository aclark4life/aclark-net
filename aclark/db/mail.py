from django.core.mail import send_mail


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
    elif model_name == 'project':
        return [(i.first_name, i.email) for i in obj.team.all()]
    elif model_name == 'time':
        return [('Alex', 'aclark@aclark.net')]


def mail_create(obj, **kwargs):
    """
    Create message and subject based on object type, else create test
    """
    first_name = kwargs.get('first_name')
    hostname = kwargs.get('hostname')
    mail_from = kwargs.get('mail_from')
    mail_to = kwargs.get('mail_to')
    message = kwargs.get('message', 'test')
    subject = kwargs.get('subject', 'test')
    model_name = obj._meta.verbose_name
    if model_name == 'time':
        message = '%s' % obj.get_absolute_url(hostname)
        subject = 'Time entry'
    elif model_name == 'project':
        subject = 'Time entry reminder'
        message = '%s,\n\nPlease enter time for: \n\n\t - %s\n\nThank you,\n\n%s' % (
            first_name, obj.name, 'https://aclark.net/db')
    context = {}
    context['mail_from'] = mail_from
    context['mail_to'] = mail_to
    context['message'] = message
    context['subject'] = subject
    return context


def mail_proc(obj, request, **kwargs):
    """
    Iterate over recipients, create message, send to each
    """
    hostname = request.META.get('HTTP_HOST')
    recipients = get_recipients(obj)
    for first_name, email_address in recipients:
        mail_send(**mail_create(
            obj,
            first_name=first_name,
            hostname=hostname,
            mail_from='aclark@aclark.net',
            mail_to=email_address,
            request=request))


def mail_send(**kwargs):
    """
    Call Django send_mail
    """
    mail_from = kwargs.get('mail_from', 'aclark@aclark.net')
    mail_to = kwargs.get('mail_to', 'aclark@aclark.net')
    message = kwargs.get('message', 'test')
    subject = kwargs.get('subject', 'test')
    send_mail(subject, message, mail_from, (mail_to, ), fail_silently=False)
