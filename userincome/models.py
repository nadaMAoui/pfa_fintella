from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.utils import timezone
import json
# Create your models here.
class Income(models.Model):
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

    class Meta:
        ordering = ['-date']

        
class Type(models.Model):
    name = models.CharField(max_length=255) 
    def __str__(self):
        return self.name   