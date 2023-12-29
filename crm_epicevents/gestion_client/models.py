from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    USERNAME_FIELD = 'username'
    nom_complet = models.CharField(max_length=255, unique=True, null=False)
    username = models.CharField(max_length=150, unique=True, null=False)
    ROLE_CHOICES = [
        ('commercial', 'Commercial'),
        ('support', 'Support'),
        ('gestion', 'Gestion'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, null=False)

    def __str__(self):
        return self.nom_complet


class Client(models.Model):
    nom_complet = models.CharField(max_length=255, null=False)
    email = models.EmailField(unique=True, null=False)
    telephone = models.CharField(max_length=12)
    entreprise = models.CharField(max_length=255, default="Particulier")
    date_creation = models.DateTimeField(auto_now_add=True)
    date_derniere_maj = models.DateField(auto_now=True, null=False)

    def __str__(self):
        return self.nom_complet


class Contrat(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=False)
    commercial = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    montant_total = models.FloatField(null=False)
    montant_restant = models.FloatField(null=False)
    date_creation = models.DateField(auto_now_add=True)
    STATUT_CHOICES = [
        ('attente signature', 'Attente de signature'),
        ('signé', 'Signé'),
        ('en cours', 'En cours'),
        ('terminé', 'Terminé'),
        ('résilié', 'Résilié'),
        ('annulé', 'Annulé'),
    ]
    statut = models.CharField(max_length=50, choices=STATUT_CHOICES, null=False)

    def __str__(self):
        return f"Contrat {self.id} - {self.client}"


class Evenement(models.Model):
    contrat = models.ForeignKey(Contrat, on_delete=models.CASCADE, null=False)
    nom = models.CharField(max_length=255, null=False)
    date_debut = models.DateField(null=False)
    date_fin = models.DateField(null=False)
    support = models.ForeignKey(User, on_delete=models.PROTECT)
    lieu = models.CharField(max_length=255, null=False)
    nombre_participants = models.IntegerField()
    notes = models.TextField()

    def __str__(self):
        return f"Événement {self.id} - {self.nom}"
