from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger


def paginate(items, orphans=None, page_num=None, page_size=None):
    """
    Paginate items
    """
    # Get a paginator
    try:
        paginator = Paginator(items, page_size, orphans=orphans)
    except TypeError:
        try:
            paginator = Paginator(items, page_size, orphans=0)
        except TypeError:
            paginator = Paginator(items, 10, orphans=0)
    # Get paginated items
    try:
        items = paginator.page(page_num)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)
    return items
