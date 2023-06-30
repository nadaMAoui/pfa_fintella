from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Bilan, Type
from django.contrib import messages
from django.core.paginator import Paginator
import datetime
from django.http import JsonResponse
import json

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Bilan, Type
from django.contrib import messages
from django.core.paginator import Paginator
import datetime
from django.http import JsonResponse
import json
# Create your views here.

def search_income(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        bilan = Bilan.objects.filter(
            actif_immobilisé__istartswith=search_str, owner=request.user) | Bilan.objects.filter(
            stock__istartswith=search_str, owner=request.user) | Bilan.objects.filter(
            créances__istartswith=search_str, owner=request.user) | Bilan.objects.filter(
            trésorerie_actif__istartswith=search_str, owner=request.user) | Bilan.objects.filter(
            capitaux_propre__istartswith=search_str, owner=request.user) | Bilan.objects.filter(
            dette_de_financement__istartswith=search_str, owner=request.user) | Bilan.objects.filter(
            dette_à_court_terme__istartswith=search_str, owner=request.user) | Bilan.objects.filter(
            type__icontains=search_str, owner=request.user(
            date__istartswith=search_str, owner=request.user) | Bilan.objects.filter)
        data = bilan.values()
        return JsonResponse(list(data), safe=False)


@login_required(login_url='/authentication/login')
def index(request):
    types = Type.objects.all()
    bilans = Bilan.objects.filter(owner=request.user)
    paginator = Paginator(bilans, 2)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    context = {
        'bilans': bilans,
        'page_obj': page_obj,
        'diagnostic_list': diagnostic_list,
        'diagnostic_two_total' : diagnostic_two_total
    }
    return render(request, 'finance/index.html', context)

def add_income(request):
    types = Type.objects.all()
    context = {
        'types': types,
        'value': request.POST 
    }
    if request.method == 'GET':
        return render(request, 'finance/add_bilan.html', context)

    if request.method == 'POST':
        actif_immobilisé = request.POST['actif_immobilisé']

        if not actif_immobilisé:
            messages.error(request, 'Actif immobilisé is required')
            return render(request, 'finance/add_bilan.html', context)
        stock = request.POST['stock']
        créances = request.POST['créances']
        trésorerie_actif = request.POST['trésorerie_actif']
        capitaux_propre = request.POST['capitaux_propre']
        dette_de_financement = request.POST['dette_de_financement']
        dette_à_court_terme = request.POST['dette_à_court_terme']
        type = request.POST['type']
        date = request.POST['bilan_date']

        if not stock:
            messages.error(request, 'Stock is required')
            return render(request, 'finance/add_bilan.html', context)
        if not créances:
            messages.error(request, 'Créances is required')
            return render(request, 'finance/add_bilan.html', context)
        if not trésorerie_actif:
            messages.error(request, 'Trésorerie is required')
            return render(request, 'finance/add_bilan.html', context)
        if not capitaux_propre:
            messages.error(request, 'Capitaux propre is required')
            return render(request, 'finance/add_bilan.html', context)
        if not dette_de_financement:
            messages.error(request, 'dette de financement is required')
            return render(request, 'finance/add_bilan.html', context)
        if not dette_à_court_terme:
            messages.error(request, 'Dette à court terme is required')
            return render(request, 'finance/add_bilan.html', context)


        Bilan.objects.create(owner=request.user, actif_immobilisé=actif_immobilisé, stock=stock, créances=créances, trésorerie_actif=trésorerie_actif, capitaux_propre=capitaux_propre, dette_de_financement=dette_de_financement, dette_à_court_terme=dette_à_court_terme, type=type, date=date)

        messages.success(request, 'Bilan saved successffully')

        return redirect('finance')
    

def income_edit(request, id):
    bilan = Bilan.objects.get(pk=id)
    types = Type.objects.all()
    context = {
        'bilan' : bilan,
        'values' : bilan,
        'types' : types
    }
    if request.method=='GET':
        return render(request, 'finance/edit-bilan.html', context)
 
    if request.method == 'POST':
        actif_immobilisé = request.POST['actif_immobilisé']

        if not actif_immobilisé:
            messages.error(request, 'Actif immobilisé is required')
            return render(request, 'finance/edit-bilan.html', context)
        stock = request.POST['stock']
        créances = request.POST['créances']
        trésorerie_actif = request.POST['trésorerie_actif']
        capitaux_propre = request.POST['capitaux_propre']
        dette_de_financement = request.POST['dette_de_financement']
        dette_à_court_terme = request.POST['dette_à_court_terme']
        type = request.POST['type']
        date = request.POST['bilan_date']

        if not stock:
            messages.error(request, 'Stock is required')
            return render(request, 'finance/edit-bilan.html', context)
        if not créances:
            messages.error(request, 'Créances is required')
            return render(request, 'finance/edit-bilan.html', context)
        if not trésorerie_actif:
            messages.error(request, 'Trésorerie is required')
            return render(request, 'finance/edit-bilan.html', context)
        if not capitaux_propre:
            messages.error(request, 'Capitaux propre is required')
            return render(request, 'finance/edit-bilan.html', context)
        if not dette_de_financement:
            messages.error(request, 'dette de financement is required')
            return render(request, 'finance/edit-bilan.html', context)
        if not dette_à_court_terme:
            messages.error(request, 'Dette à court terme is required')
            return render(request, 'finance/edit-bilan.html', context)


        bilan.owner = request.user
        bilan.stock = stock
        bilan.créances = créances
        bilan.trésorerie_actif = trésorerie_actif
        bilan.capitaux_propre = capitaux_propre
        bilan.dette_de_financement = dette_de_financement
        bilan.dette_à_court_terme = dette_à_court_terme
        bilan.type = type
        bilan.date = date

        bilan.save()
        messages.success(request, 'Bilan updated  successfully')

        return redirect('finance')

def delete_income(request, id):
    bilan = Bilan.objects.get(pk=id)
    bilan.delete()
    messages.success(request, 'Bilan removed')
    return redirect('finance')