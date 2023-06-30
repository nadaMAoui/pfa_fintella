from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Bilan, Type
from django.contrib import messages
from django.core.paginator import Paginator
import datetime
from django.http import JsonResponse,HttpResponse
import json
import csv
import xlwt

from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile
from django.http import FileResponse
# Create your views here.

def search_bilan(request):
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
    diagnostic_two_total = get_diagnostic_two(request)
    diagnostic_list = get_diagnostic(request)
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

def add_bilan(request):
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
    

def bilan_edit(request, id):
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

def delete_bilan(request, id):
    bilan = Bilan.objects.get(pk=id)
    bilan.delete()
    messages.success(request, 'Bilan removed')
    return redirect('finance')

def get_commentaire(request):
    commentaire = Bilan.objects.values_list('financement_permanent_text', 'solvabilite_general_text','capacite_de_remboursement_text', 'autonomie_financiere_text')
    commentaire_list = list(commentaire)
    return commentaire_list
     
def get_diagnostic_two(request):
    diagnostic_two = Bilan.objects.values('actif', 'passif','fond_de_roulement', 'besoin_de_fond_roulement', 'tresorerie_net' )
    diagnostic_two_total = list(diagnostic_two)
    return diagnostic_two_total

def get_total_numbers(request):
    total_numbers = Bilan.objects.values('actif', 'passif')
    total_list = list(total_numbers)
    return total_list

def get_bilan(request):
    total_indicator = Bilan.objects.values('actif_immobilisé', 'stock', 'créances', 'trésorerie_actif', 'capitaux_propre', 'dette_de_financement', 'dette_à_court_terme')
    bilan_list = list(total_indicator)
    return bilan_list
def get_indicator(request):
    total_indicator = Bilan.objects.values('financement_permanent', 'solvabilite_general', 'capacite_de_remboursement', 'autonomie_financiere')
    indicator_list = list(total_indicator)
    return indicator_list

def get_diagnostic(request):
    total_diagnostic = Bilan.objects.values('fond_de_roulement', 'besoin_de_fond_roulement', 'tresorerie_net')
    diagnostic_list = list(total_diagnostic)
    return diagnostic_list

def bilan_summary(request):
    commentaire_list = get_commentaire(request)
    bilan_list = get_bilan(request)
    total_list = get_total_numbers(request)
    indicator_list = get_indicator(request)
    diagnostic_list = get_diagnostic(request)
    diagnostic_two_total = get_diagnostic_two(request)
    bilan = Bilan.objects.all()

    todays_date = datetime.date.today()
    six_months_ago = todays_date - datetime.timedelta(days=30*6)
    bilan = Bilan.objects.filter(owner=request.user,
                                 date__gte=six_months_ago, date__lte=todays_date)

    return JsonResponse({
        'total_indicator': bilan_list, 
        'total_numbers': total_list,
        'indicator_list': indicator_list,
        'diagnostic_list': diagnostic_list,
        'diagnostic_two_total' : diagnostic_two_total,
        'commentaire_list' : commentaire_list,

    })

def stats_view(request):
    commentaire_list = get_commentaire(request)
    bilan_list = get_bilan(request)
    total_list = get_total_numbers(request)
    indicator_list = get_indicator(request)
    diagnostic_list = get_diagnostic(request)

    context = {
        'total_indicator': bilan_list, 
        'total_numbers': total_list,
        'indicator_list': indicator_list,
        'diagnostic_list': diagnostic_list,
        'commentaire_list': commentaire_list,
    }
    return render(request, 'finance/stats.html', context)

def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition']='attachment; filename-Finance' + \
        str(datetime.datetime.now())+'.csv'
    
    writer=csv.writer(response)
    writer.writerow(['Actif Immobilisé', 'Stock', 'Créances', 'Trésorerie Actif', 'Capitaux Propre', 'Dette de Financement',
                    'Dette à court Terme','passif', 'actif', 'Fond de Roulement', 'Besoin de fond Roulement', 'Tresorerie Net', 'Financement Permanent', 'Autonomie Financiere', 'Solvabilite General', 'Capacite de Remboursement', 'Type', 'Date'])


    bilans = Bilan.objects.filter(owner=request.user)

    for bilan in bilans:
        writer.writerow([bilan.actif_immobilisé, bilan.stock, bilan.créances, bilan.trésorerie_actif, bilan.capitaux_propre, bilan.dette_de_financement,
                        bilan.dette_à_court_terme, bilan.passif, bilan.actif, bilan.fond_de_roulement, bilan.besoin_de_fond_roulement, bilan.tresorerie_net, bilan.financement_permanent, bilan.autonomie_financiere, bilan.solvabilite_general, bilan.capacite_de_remboursement, bilan.type, bilan.date ])


    return response

def export_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition']='attachment; filename-Finance' + \
        str(datetime.datetime.now())+'.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Bilan')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Actif Immobilisé', 'Stock', 'Créances', 'Trésorerie Actif', 'Capitaux Propre', 'Dette de Financement',
                    'Dette à court Terme','passif', 'actif', 'Fond de Roulement', 'Besoin de fond Roulement', 'Tresorerie Net', 'Financement Permanent', 'Autonomie Financiere', 'Solvabilite General', 'Capacite de Remboursement', 'Type', 'Date']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()

    rows = Bilan.objects.filter(owner=request.user).values_list('actif_immobilisé', 'stock', 'créances', 'trésorerie_actif', 'capitaux_propre', 'dette_de_financement',
                        'dette_à_court_terme', 'passif', 'actif', 'fond_de_roulement', 'besoin_de_fond_roulement', 'tresorerie_net', 'financement_permanent', 'autonomie_financiere', 'solvabilite_general', 'capacite_de_remboursement', 'type', 'date' )

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)
    wb.save(response)

    return response        

def export_pdf(request):

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; attachment: filename=Finance' + \
        str(datetime.datetime.now())+'.pdf'
    response['Content-Transfer-Encoding'] = 'binary'

    bilans = Bilan.objects.filter(owner=request.user)

    html_string = render_to_string('finance/pdf-output.html', {'finance': bilans})
    html = HTML(string=html_string)

    result = html.write_pdf()

    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()

        output = open(output.name, 'rb')
        response.write(output.read())
    return response  

