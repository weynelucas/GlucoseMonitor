from django.shortcuts import render, redirect
from .forms import GlucoseMeasureForm
from .models import GlucoseMeasure
from django.contrib.auth.decorators import login_required
from datetime import datetime

# Create your views here.
@login_required
def index(request):

    context = {
        'measures': GlucoseMeasure.objects.filter(user_id=request.user.id).order_by('-datetime')[:10]
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
        form.datetime = datetime.now()
    return render(request, 'measures/create.html', {'form': list(form)[:3]})
