from django.http import HttpResponse
from django_xhtml2pdf.utils import generate_pdf
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from io import StringIO
from lxml import etree

DOC = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'


def render_doc(context, **kwargs):
    """
    https://stackoverflow.com/a/24122313/185820
    """
    document = Document()
    # Head
    task = ''
    contract = context['item']
    if contract.task:
        task = contract.task
    title = document.add_heading(
        'ACLARK.NET, LLC %s AGREEMENT PREPARED FOR:' % task, level=1)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    if contract.client:
        client_name = document.add_heading(contract.client.name, level=1)
        client_name.alignment = WD_ALIGN_PARAGRAPH.CENTER
        client_address = document.add_heading(contract.client.address, level=1)
        client_address.alignment = WD_ALIGN_PARAGRAPH.CENTER
    parser = etree.HTMLParser()  # http://lxml.de/parsing.html
    tree = etree.parse(StringIO(contract.body), parser)
    # Body
    for element in tree.iter():
        if element.tag == 'h2':
            document.add_heading(element.text, level=2)
        elif element.tag == 'p':
            document.add_paragraph(element.text)
    response = HttpResponse(content_type=DOC)
    response['Content-Disposition'] = 'attachment; filename=download.docx'
    document.save(response)
    return response


def render_pdf(context, **kwargs):
    filename = kwargs.get('filename', 'pdf.pdf')
    template = kwargs.get('template', 'pdf.html')
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename=%s' % filename
    return generate_pdf(template, context=context, file_object=response)
