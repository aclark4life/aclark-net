from django.http import HttpResponse
from django_xhtml2pdf.utils import generate_pdf


def render_pdf(context, **kwargs):
    filename = kwargs.get('filename', 'pdf.pdf')
    template = kwargs.get('template', 'pdf.html')
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename=%s' % filename
    return generate_pdf(template, context=context, file_object=response)
