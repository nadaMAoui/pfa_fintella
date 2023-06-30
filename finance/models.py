from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.utils import timezone
import json
# Create your models here.
class Bilan(models.Model):
    actif_immobilisé = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stock = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    créances = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    trésorerie_actif = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    capitaux_propre = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    dette_de_financement = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    dette_à_court_terme = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    type = models.CharField(max_length=266)
    date = models.DateTimeField(default=timezone.now)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    passif = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    actif = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fond_de_roulement = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    besoin_de_fond_roulement = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tresorerie_net = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    financement_permanent = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    solvabilite_general = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    capacite_de_remboursement= models.DecimalField(max_digits=10, decimal_places=2, default=0)
    autonomie_financiere = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    financement_permanent_text = models.CharField(max_length=2000, default=0)
    solvabilite_general_text = models.CharField(max_length=2000, default=0)
    capacite_de_remboursement_text = models.CharField(max_length=2000, default=0)
    autonomie_financiere_text = models.CharField(max_length=2000, default=0)

    def save(self, *args, **kwargs):
        self.passif = self.calculate_passif()
        self.actif = self.calculate_actif()
        self.fond_de_roulement = self.calculate_fond_de_roulement()
        self.besoin_de_fond_roulement = self.calculate_besoin_de_fond_roulement()
        self.tresorerie_net = self.calculate_tresorie_net()
        self.financement_permanent = self.calculate_financement_permanent()
        self.autonomie_financiere = self.calculate_autonomie_financiere()
        self.solvabilite_general  = self.calculate_solvabilite_general()
        self.capacite_de_remboursement = self.calculate_capacite_de_remboursement()
        self.financement_permanent_text = self.commentaire_financement_permanent()
        self.solvabilite_general_text = self.commentaire_autonomie_financiére()
        self.capacite_de_remboursement_text = self.commentaire_capacité_de_remboursement()
        self.autonomie_financiere_text = self.commentaire_autonomie_financiére()

        super().save(*args, **kwargs)


    def calculate_passif(self):
        try:
            capitaux_propre = float(self.capitaux_propre)
            dette_de_financement = float(self.dette_de_financement)
            dette_à_court_terme = float(self.dette_à_court_terme)
            if capitaux_propre is not None and dette_de_financement is not None and dette_à_court_terme is not None:
                passif = capitaux_propre + dette_de_financement + dette_à_court_terme
                return passif
        except (ValueError, TypeError):
            pass
        return 0

    def calculate_actif(self):
        try:
            actif_immobilisé = float(self.actif_immobilisé)
            stock = float(self.stock)
            créances = float(self.créances)
            trésorerie_actif = float(self.trésorerie_actif)
            if actif_immobilisé is not None and stock is not None and créances is not None and trésorerie_actif is not None:
                actif = (actif_immobilisé + stock ) + (créances + trésorerie_actif)
                return actif
        except (ValueError, TypeError):
            pass
        return 0

    def calculate_fond_de_roulement(self):
        try:
            capitaux_propre = float(self.capitaux_propre)
            dette_de_financement = float(self.dette_de_financement)
            dette_a_court_terme = float(self.dette_à_court_terme)
            if capitaux_propre is not None and dette_de_financement is not None and dette_a_court_terme is not None:
                fond_de_roulemnt = capitaux_propre + dette_de_financement - dette_a_court_terme
                return fond_de_roulemnt
        except (ValueError, TypeError):
            pass
        return 0

    def calculate_besoin_de_fond_roulement(self):
        try:
            stock = float(self.stock)
            créances = float(self.créances)
            dette_a_court_terme = float(self.dette_à_court_terme)
            if stock is not None and créances is not None and dette_a_court_terme is not None:
                besoin_de_fond_roulemnt = (stock + créances) - dette_a_court_terme
                return besoin_de_fond_roulemnt
        except (ValueError, TypeError):
            pass
        return 0                    
    
    def calculate_tresorie_net(self):
        try:
            fond_de_roulemnt = float(self.fond_de_roulement)
            besoin_de_fond_roulemnt = float(self.besoin_de_fond_roulement)
            if fond_de_roulemnt is not None and besoin_de_fond_roulemnt is not None:
                tresorerie_net = fond_de_roulemnt - besoin_de_fond_roulemnt
                return tresorerie_net
        except (ValueError, TypeError):
            pass
        return 0

    
    def calculate_financement_permanent(self):
        try:
            actif_immobilisé = float(self.actif_immobilisé)
            capitaux_propre = float(self.capitaux_propre)
            dette_de_financement = float(self.dette_de_financement)
            if actif_immobilisé != 0 and capitaux_propre is not None and dette_de_financement is not None:
                financement_permanent = (capitaux_propre + dette_de_financement) / actif_immobilisé
                return financement_permanent
        except (ValueError, TypeError):
            pass
        return 0

    
    def calculate_autonomie_financiere(self):
        try:
            dette_de_financement = float(self.dette_de_financement)
            capitaux_propre = float(self.capitaux_propre)
            if dette_de_financement != 0 and capitaux_propre != 0 and capitaux_propre is not None and dette_de_financement is not None:
                autonomie_financiere = capitaux_propre / (dette_de_financement + capitaux_propre)
                return autonomie_financiere
        except (ValueError, TypeError):
            pass
        return 0

    
    def calculate_solvabilite_general(self):
        try:
            actif = float(self.actif)
            dette_a_court_terme = float(self.dette_à_court_terme)
            dette_de_financement = float(self.dette_de_financement)
            if dette_a_court_terme != 0 and dette_de_financement != 0 and actif is not None:
                solvabilite_generale = actif / (dette_a_court_terme + dette_de_financement)
                return solvabilite_generale
        except ValueError:
            pass
        return 0

    
    def calculate_capacite_de_remboursement(self):
        try:
            dette_de_financement = float(self.dette_de_financement)
            capitaux_propre = float(self.capitaux_propre)
            if dette_de_financement != 0 and capitaux_propre is not None:
                capacite_de_remboursement = capitaux_propre / dette_de_financement
                return capacite_de_remboursement
        except (ValueError, TypeError):
            pass
        return 0
    
    def commentaire_financement_permanent(self):
        financement_permanent = float(self.financement_permanent)
        if financement_permanent < 1:
            return "Financement Permanent < 0: l'entreprise ne dispose pas d'un équilibre"
        else:
            return "Financement permanent > 0: l'actif immobilisé est financé par les capitaux propres et l'entreprise possède des capitaux permanents supplémentaires pour financer des besoins d'exploitation."
    def commentaire_autonomie_financiére(self):
        autonomie_financiére = float(self.autonomie_financiere)
        if autonomie_financiére > 0.5:
            return "l'entreprise est indépendant vis-à-vis de ses créancier"
        else:
            return "l'entreprise est en manque de capitaux."

    def commentaire_solvabilité_géneral(self):
        solvabilité_géneral = float(self.solvabilite_general)
        if solvabilité_géneral > 1:
            return "l'entreprise est solvable."
        else:
            return "l'entreprise n'est pas solvable."

    def commentaire_capacité_de_remboursement(self):
        capacite_de_remboursement = float(self.capacite_de_remboursement)
        if capacite_de_remboursement > 1 :
            return "l'entreprise peut rembourser ses dette "
        else:
            return "les revenus disponibles ne suffisent pas à couvrir vos dépenses de remboursement."           
    
    class Meta:
        ordering = ['-date']

        
class Type(models.Model):
    name = models.CharField(max_length=255) 
    def __str__(self):
        return self.name