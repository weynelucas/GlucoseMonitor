from datetime import datetime, timedelta, time
from django.http import Http404

period_choices = ['30', '60', 'today', 'all', 'custom']

def period_param_is_valid(view_function):
    """ Decorator to evaluate the period params on request
        before execute the view function
    """
    def wrap(request, *args, **kwargs):
        period, period_begin, period_end = get_period_params(request)
        if period not in period_choices or ((period == 'custom') and (not period_begin or not period_end)):
            raise Http404
        return view_function(request, *args, **kwargs)

    return wrap


def get_period_interval(request):
    """ Get the period interval (begin and end) given
        the request object

        Args:
            request: HttpRequestObject
        Returns:
            Period interval (period_begin and period_end)
            as a datetime list
    """
    period = request.GET.get('period', '30')
    today = datetime.now()
    final_date   = datetime.combine(today, time.max)
    try:
        days_left = int(period)
        initial_date = datetime.combine(today - timedelta(days=days_left), time.min)
    except ValueError:
        if period == 'all':
            initial_date = datetime.combine(request.user.date_joined, time.min)
        elif period == 'custom':
            initial_date = datetime.combine(datetime.strptime(request.GET['period_begin'], '%d/%m/%Y'), time.min)
            final_date   = datetime.combine(datetime.strptime(request.GET['period_end'], '%d/%m/%Y'), time.max)
        elif period == 'today':
            initial_date = datetime.combine(today, time.min)


    return [initial_date, final_date]


def get_period_params(request):
    """ Get the period params on request

        Args:
            request: HttpRequestObject
        Returns:
            List of period parameters (period, period_begin and
            period_end) as a list of strings
    """
    period = request.GET.get('period', '30')
    period_begin = ''
    period_end = ''
    if period == 'custom':
        period_begin = request.GET.get('period_begin', '')
        period_end = request.GET.get('period_end', '')

    return [period, period_begin, period_end]
