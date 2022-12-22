from django.core.paginator import Paginator


QUAN_POST: int = 10


def paginator(request, post_list):
    paginator = Paginator(post_list, QUAN_POST)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj
