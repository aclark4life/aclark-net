def get_query_string(request, key):
    """
    Return calculated values for some query string keys, else return value.
    """
    if key == 'paginated':
        paginated = request.GET.get('paginated')
        if paginated == u'false':
            return False
        else:
            return True
    elif key == 'search' and request.method == 'POST':
        return request.POST.get('search', '')
    elif key == 'costs':  # plot
        costs = request.GET.get('costs')
        if costs:
            costs = costs.split(' ')
        else:
            costs = []
        costs = [i.split(',') for i in costs]
        return costs
    elif key == 'grosses':  # plot
        grosses = request.GET.get('grosses')
        if grosses:
            grosses = grosses.split(' ')
        else:
            grosses = []
        grosses = [i.split(',') for i in grosses]
        return grosses
    elif key == 'nets':  # plot
        nets = request.GET.get('nets')
        if nets:
            nets = nets.split(' ')
        else:
            nets = []
        nets = [i.split(',') for i in nets]
        return nets
    elif key == 'checkbox':
        query_checkbox = {}
        query_checkbox_active = request.POST.get('checkbox-active')
        query_checkbox_subscribe = request.POST.get('checkbox-subscribe')
        condition = (  # if any of these exist
            query_checkbox_active == 'on' or query_checkbox_active == 'off'
            or query_checkbox_subscribe == 'on'
            or query_checkbox_subscribe == 'off')
        query_checkbox['active'] = query_checkbox_active
        query_checkbox['subscribe'] = query_checkbox_subscribe
        query_checkbox['condition'] = condition
        return query_checkbox
    elif key == 'copy':
        return request.POST.get('copy')
    elif key == 'delete':
        return request.POST.get('delete')
    elif key == 'invoiced':
        query_invoiced = {}
        query_invoiced_state = request.POST.get('invoiced')
        query_invoiced['state'] = query_invoiced_state
        condition = (  # if either of these exist
            query_invoiced_state == 'true' or query_invoiced_state == 'false')
        query_invoiced['condition'] = condition
        return query_invoiced
    else:
        return request.GET.get(key)
