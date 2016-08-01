from measures.models import GlucoseMeasure
from measures.period import get_period_interval

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
