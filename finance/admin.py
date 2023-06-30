
from django.contrib import admin
from .models import Bilan, Type

class BilanAdminSite(admin.ModelAdmin):
    model = Bilan
    
    fields = ['actif_immobilisé', 'stock', 'créances', 'trésorerie_actif', 'capitaux_propre', 'dette_de_financement',
'dette_à_court_terme', 'passif', 'actif', 'fond_de_roulement', 'besoin_de_fond_roulement', 'tresorerie_net', 'financement_permanent', 'autonomie_financiere', 'solvabilite_general', 'capacite_de_remboursement', 'financement_permanent_text', 'solvabilite_general_text','capacite_de_remboursement_text', 'autonomie_financiere_text'  ]
    list_display = (
'actif_immobilisé', 'stock', 'créances', 'trésorerie_actif', 'capitaux_propre', 'dette_de_financement',
'dette_à_court_terme', 'passif', 'actif', 'fond_de_roulement', 'besoin_de_fond_roulement', 'tresorerie_net', 'financement_permanent', 'autonomie_financiere', 'solvabilite_general', 'capacite_de_remboursement', 'financement_permanent_text', 'solvabilite_general_text', 'capacite_de_remboursement_text', 'autonomie_financiere_text'
)


admin.site.register(Bilan, BilanAdminSite)
admin.site.register(Type)