import json
from datetime import datetime, timedelta, time
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from measures.encoders import DecimalEncoder, DateTimeEncoder
from measures.forms import GlucoseMeasureForm
from measures.models import GlucoseMeasure
from measures.report.generator import ReportGenerator
from measures.querybusiness import peform_query
from measures.period import get_period_params, get_period_interval, period_param_is_valid
from django.db.models import Avg, Max, Min
from django.utils import timezone

@login_required
@period_param_is_valid
def index(request):
    if request.method == 'POST':
        path = request.META['HTTP_REFERER']
        form = GlucoseMeasureForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Medição adicionada com sucesso')
            return redirect(path)
    else:
        form = GlucoseMeasureForm()

    # Listen period
    period, period_begin, period_end = get_period_params(request)

    # Get queryset
    queryset = peform_query(request)

    # Measure type queryset separation
    fst_queryset = queryset.filter(measure_type='FST')
    afm_queryset = queryset.filter(measure_type='AFM')

    # Projections data
    values     = list(queryset.reverse().values_list('value', flat=True))
    datetimes  = list(queryset.reverse().values_list('datetime', flat=True))

    # Context dict
    context = {
        'form'        : form,
        'period'      : period,
        'period_begin': period_begin,
        'period_end'  : period_end,
        'tab'         : 'home',
        'queryset'    : queryset,
        'last'        : queryset[:5],
        'distribution': {
            'hypo': fst_queryset.filter(value__lte=70).count() + afm_queryset.filter(value__lte=70).count(),
            'norm': fst_queryset.filter(value__gt=70,  value__lte=100).count() + afm_queryset.filter(value__gt=70,  value__lte=140).count(),
            'pre' : fst_queryset.filter(value__gt=100, value__lte=126).count() + afm_queryset.filter(value__gt=140, value__lte=200).count(),
            'high': fst_queryset.filter(value__gt=126).count() + afm_queryset.filter(value__gt=200).count(),
        },
        'overlay': {
            'data'  : json.dumps(values,    cls=DecimalEncoder),
            'labels': json.dumps(datetimes, cls=DateTimeEncoder),
        },
        'average': queryset.aggregate(Avg('value'))['value__avg'],
        'max'    : queryset.aggregate(Max('value'))['value__max'],
        'min'    : queryset.aggregate(Min('value'))['value__min'],
    }

    return render(request, 'measures/index.html', context)



@login_required
@period_param_is_valid
def measures_list(request):
    queryset = peform_query(request)
    period, period_begin, period_end = get_period_params(request)

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
        'tab'         : 'list',
        'period'      : period,
        'period_begin': period_begin,
        'period_end'  : period_end,
        'queryset'    : paginated_list,
    }
    return render(request, 'measures/list.html', context)


@login_required
def delete_measure (request, id):
    # Get path to return
    path = request.META.get('HTTP_REFERER', 'measures/list')
    # User only can delete your own measures
    instance = get_object_or_404(GlucoseMeasure, pk=id)
    if instance.user.id != request.user.id:
        raise Http404

    instance.delete()
    messages.success(request, 'Medição excluída com sucesso')
    return redirect(path)


@login_required
def edit_measure(request, id):
    # Get path to return
    path = request.META['HTTP_REFERER']
    # User only can edit your own measures
    instance = get_object_or_404(GlucoseMeasure, pk=id)
    if instance.user.id != request.user.id:
        raise Http404

    form =  GlucoseMeasureForm(request.POST or None, instance=instance)

    if request.method == 'POST':
        path = request.POST.get('return_path', '/measures/list')
        if form.is_valid():
            form.save()
            messages.success(request, 'Medição editada com sucesso')
            return redirect(path)

    context = {
        'form': form,
        'return_path': path,
    }
    return render(request, 'measures/edit.html', context)

@login_required
@period_param_is_valid
def export_pdf(request):
    queryset = peform_query(request)
    period_interval = get_period_interval(request)

    response = HttpResponse(content_type='application/pdf')
    filename = 'Relatorio_' + timezone.now().strftime('%Y_%m_%d__%H_%M')
    response['Content-Disposition'] ='attachement; filename=%s.pdf' % (filename)

    report = ReportGenerator()
    pdf = report.generatePdfReport(queryset, period_interval)
    response.write(pdf)
    return response
