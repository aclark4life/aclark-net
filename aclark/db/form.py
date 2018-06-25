from django.shortcuts import get_object_or_404
from django.utils import timezone
from .query import get_query_string
from .total import get_total


def get_form(**kwargs):
    """
    Return appropriate form based on new or edit
    """
    client_model = kwargs.get('client_model')
    form_model = kwargs.get('form_model')
    invoice_model = kwargs.get('invoice_model')
    model = kwargs.get('model')
    obj = kwargs.get('obj')
    request = kwargs.get('request')
    project_model = kwargs.get('project_model')
    user_model = kwargs.get('user_model')
    query_client = None
    query_project = None
    query_user = None
    if request:
        query_user = get_query_string(request, 'user')
        query_client = get_query_string(request, 'client')
    if obj:  # Existing object
        model_name = obj._meta.verbose_name
        if model_name == 'note':  # Populate form with tags already set
            form = form_model(initial={'tags': obj.tags.all()}, instance=obj)
        elif model_name == 'time':  # XXX Dup
            projects = project_model.objects.filter(
                team__in=[request.user.pk], active=True)
            choices = [('', '---------')]
            for project in projects:
                choice = (("%s" % project.id, "%s" % project))
                choices.append(choice)
            form = form_model(instance=obj)
            form.fields['project'].widget.choices = choices
        else:
            form = form_model(instance=obj)
    else:  # New object
        if model:
            model_name = model._meta.verbose_name
            if model_name == 'report' and invoice_model:  # Populate new report
                # with gross
                invoices = invoice_model.objects.filter(last_payment_date=None)
                projects = project_model.objects.filter(invoice__in=invoices)
                gross = get_total(field='amount', invoices=invoices)['amount']
                cost = get_total(field='cost', projects=projects)['cost']
                net = gross - cost
                obj = model(cost=cost, gross=gross, net=net)
                form = form_model(instance=obj, initial={'invoices': invoices})
            elif model_name == 'contact':  # Populate new contact
                # with appropriate fields
                if query_client:
                    client = get_object_or_404(client_model, pk=query_client)
                    obj = model(client=client)
                form = form_model(instance=obj)
            elif model_name == 'estimate':
                if query_user:
                    user = get_object_or_404(user_model, pk=query_user)
                    obj = model(user=user)
                elif query_project:
                    project = get_object_or_404(
                        project_model, pk=query_project)
                    obj = model(project=project)
                form = form_model(instance=obj)
            elif model_name == 'invoice':
                client = get_object_or_404(client_model, pk=query_client)
                now = timezone.now()
                obj = model(subject="%s %s" % (client, now.strftime('%B %Y')))
                form = form_model(instance=obj)
            elif model_name == 'time':  # XXX Dup
                projects = project_model.objects.filter(
                    team__in=[request.user.pk], active=True)
                choices = [('', '---------')]
                for project in projects:
                    choice = (("%s" % project.id, "%s" % project))
                    choices.append(choice)
                form = form_model()
                form.fields['project'].widget.choices = choices
            else:
                form = form_model()
        else:
            form = form_model()
    return form
