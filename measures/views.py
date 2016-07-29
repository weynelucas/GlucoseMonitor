import json
from datetime import datetime, timedelta, time
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from measures.encoders import DecimalEncoder, DateTimeEncoder
from measures.forms import GlucoseMeasureForm
from measures.models import GlucoseMeasure


@login_required
def index(request):
    if request.method == 'POST':
        form = GlucoseMeasureForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Medição adicionada com sucesso')
            return redirect(index)
    else:
        form = GlucoseMeasureForm()

    # Generate query period
    today = datetime.now()
    final_date   = datetime.combine(today, time.max)
    initial_date = datetime.combine(today - timedelta(days=30), time.min)

    queryset = GlucoseMeasure.objects.filter(
        user__id      = request.user.id,
        datetime__gte = initial_date,
        datetime__lte = final_date
    ).order_by('-datetime')

    # Measure type queryset separation
    fst_queryset = queryset.filter(measure_type='FST')
    afm_queryset = queryset.filter(measure_type='AFM')

    # Projections data
    values     = list(queryset.reverse().values_list('value', flat=True))
    datetimes  = list(queryset.reverse().values_list('datetime', flat=True))

    # Context dict
    context = {
        'form': form,
        'queryset': queryset,
        'last'    : queryset[:5],
        'distribution': {
            'hypo': fst_queryset.filter(value__lte=70).count() + afm_queryset.filter(value__lte=70).count(),
            'norm': fst_queryset.filter(value__gt=70,  value__lte=100).count() + afm_queryset.filter(value__gt=70,  value__lte=140).count(),
            'pre' : fst_queryset.filter(value__gt=100, value__lte=126).count() + afm_queryset.filter(value__gt=140, value__lte=200).count(),
            'high': fst_queryset.filter(value__gt=126).count() + afm_queryset.filter(value__gt=200).count(),
        },
        'overlay': {
            'data'  : json.dumps(values,    cls=DecimalEncoder),
            'labels': json.dumps(datetimes, cls=DateTimeEncoder),
        }
    }

    return render(request, 'measures/index.html', context)



@login_required
def measures_list(request):
    # Generate query period
    today = datetime.now()
    final_date   = datetime.combine(today, time.max)
    initial_date = datetime.combine(today - timedelta(days=30), time.min)

    queryset = GlucoseMeasure.objects.filter(
        user__id      = request.user.id,
        datetime__gte = initial_date,
        datetime__lte = final_date
    ).order_by('-datetime')

    # Prepare paginator
    paginator = Paginator(queryset, 15)
    page = request.GET.get('page', 1)

    # Paginate queryset
    try:
        paginated_list = paginator.page(page)
    except PageNotAnInteger:
        paginated_list = paginator.page(1)
    except EmptyPage:
        paginated_list = paginator.page(paginator.num_pages)

    context = {
        'queryset': paginated_list,
    }
    return render(request, 'measures/list.html', context)
