from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger


def paginate(items, page=None, page_size=None):
    """
    """
    if page is None:
        page = 1
    if page_size is not None:
        paginator = Paginator(items, page_size, orphans=5)
    else:
        paginator = Paginator(items, 10, orphans=5)
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)
    return items
