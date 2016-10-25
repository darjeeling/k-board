

def get_pages_nav_info(page, nav_chunk_size=10):
    """ this function return navigation bar info of paginated objects """

    first_page_in_list = (
        int((page.number - 1) / nav_chunk_size)) * nav_chunk_size + 1
    end_page_in_list = (
        int((page.number - 1) / nav_chunk_size) + 1) * nav_chunk_size
    page_list = []
    for page_num in range(first_page_in_list, end_page_in_list + 1):
        if page_num > page.paginator.num_pages:
            break
        page_list.append(page_num)

    # if not exist nav_page, -1
    pre_nav_page = -1
    next_nav_page = -1

    if page.number > nav_chunk_size:
        pre_nav_page = first_page_in_list - 1

    if end_page_in_list < page.paginator.num_pages:
        next_nav_page = end_page_in_list + 1

    pages_nav_info = {
        'pre_nav_page': pre_nav_page,
        'page_list': page_list,
        'current_page_num': page.number,
        'next_nav_page': next_nav_page}
    return pages_nav_info
