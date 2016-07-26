from django.shortcuts import render, redirect
from .forms import GlucoseMeasureForm
from .models import GlucoseMeasure
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime

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
    queryset     = GlucoseMeasure.objects.filter(user__id=request.user.id).order_by('-datetime')[:6]
    hypoglycemia = len(GlucoseMeasure.objects.filter(user__id=request.user.id, value__lt=71))
    normal       = len(GlucoseMeasure.objects.filter(user__id=request.user.id, value__gt=70, value__lt=101))
    pre_diabetes = len(GlucoseMeasure.objects.filter(user__id=request.user.id, value__gt=100, value__lt=127))
    diabetes     = len(GlucoseMeasure.objects.filter(user__id=request.user.id, value__gt=126))


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
