from django.shortcuts import render, redirect
from .forms import GlucoseMeasureForm
from .models import GlucoseMeasure
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
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

    # Stats queries
    queryset     = GlucoseMeasure.objects.filter(user__id=request.user.id).order_by('-datetime')[:5]
    hypoglycemia = GlucoseMeasure.objects.filter(user__id=request.user.id, value__lte=70).count()
    normal       = GlucoseMeasure.objects.filter(user__id=request.user.id, value__gt=70, value__lte=100).count()
    pre_diabetes = GlucoseMeasure.objects.filter(user__id=request.user.id, value__gt=100, value__lte=126).count()
    diabetes     = GlucoseMeasure.objects.filter(user__id=request.user.id, value__gt=126).count()


    context = {
        'form': form,
        'queryset': queryset,
        'measures_stats': {
            'hypoglycemia': hypoglycemia,
            'normal': normal,
            'pre_diabetes': pre_diabetes,
            'diabetes': diabetes,
        },
    }
    return render(request, 'measures/index.html', context)

@login_required
def list(request):
    initial_date = datetime.strptime(request.GET.get('initial_date','11/06/2016 00:00'), "%d/%m/%Y %H:%M").date()
    final_date = datetime.strptime(request.GET.get('finall_date','11/06/2030 00:00'), "%d/%m/%Y %H:%M").date()
    queryset = GlucoseMeasure.objects.filter(datetime__gte=initial_date, datetime__lte=final_date)
    paginator = Paginator(queryset, 15)
    page = request.GET.get('page', 1)

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


@login_required
def create(request):
    if request.method == 'POST':
        form = GlucoseMeasureForm(request.POST)
        print(form.errors)
        if form.is_valid():
            form.save()
            return redirect(index)
    else:
        form = GlucoseMeasureForm()
    return render(request, 'measures/create.html', {'form': list(form)[:3]})
