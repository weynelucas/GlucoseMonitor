from datetime import datetime, timedelta, time
from measures.models import GlucoseMeasure

def peform_query(request):
    """ Perform a query in GlucoseMeasure given the period and
        the logged user present on the request object

        Args:
            request: HttpRequest object
        Returns:
            List of objects (queryset) given the arguments
    """
    period_interval = get_period_interval(request)

    queryset = GlucoseMeasure.objects.filter(
        user__id      = request.user.id,
        datetime__gte = period_interval[0],
        datetime__lte = period_interval[1]
    ).order_by('-datetime')

    return queryset


def get_period_interval(request):
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
            initial_date = datetime.strptime(request.GET['period_begin'], '%d/%m/%Y')
            final_date   = datetime.strptime(request.GET['period_end'], '%d/%m/%Y')

    return [initial_date, final_date]
