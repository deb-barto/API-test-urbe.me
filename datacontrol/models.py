from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum, Avg

class ClientSummary(models.Model):
    BROKER_CHOICES = [
        ('A', 'Corretora A'),
        ('B', 'Corretora B'),
        ('C', 'Corretora C'),
    ]
    name = models.CharField(max_length=255)
    broker = models.CharField(max_length=1, choices=BROKER_CHOICES, default='A')

    def calculate_total(self):
        transactions = self.transactions.all()
        total = sum(t.value for t in transactions if t.transaction_type == "Aporte") - \
                sum(t.value for t in transactions if t.transaction_type == "Resgate")
        return total
    
    def __str__(self):
        return self.name 
    
class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('Aporte', 'Aporte'),
        ('Resgate', 'Resgate'),
    ]
    client = models.ForeignKey(ClientSummary, related_name='transactions', on_delete=models.CASCADE)
    date = models.DateField()
    value = models.FloatField()
    transaction_type = models.CharField(max_length=7, choices=TRANSACTION_TYPE_CHOICES)

@receiver(post_save, sender=Transaction)
def update_client_value(sender, instance, **kwargs):
    update_advisor_summary()

def update_advisor_summary():
    total_equity = Transaction.objects.filter(transaction_type='Aporte').aggregate(Sum('value'))['value__sum'] or 0
    total_equity -= Transaction.objects.filter(transaction_type='Resgate').aggregate(Sum('value'))['value__sum'] or 0
    average_equity = total_equity / ClientSummary.objects.count() if ClientSummary.objects.count() > 0 else 0
    total_clients = ClientSummary.objects.count()

    AdvisorSummary.objects.update_or_create(
        id=1, 
        defaults={
            'total_equity': total_equity,
            'average_equity': average_equity,
            'total_clients': total_clients,
        }
    )

class AdvisorSummary(models.Model):
    total_equity = models.FloatField(default=0.0)
    average_equity = models.FloatField(default=0.0)
    total_clients = models.IntegerField(default=0)

@receiver(post_save, sender=ClientSummary)
@receiver(post_delete, sender=ClientSummary)
@receiver(post_save, sender=Transaction)
@receiver(post_delete, sender=Transaction)
def advisor_summary_update(sender, instance, **kwargs):
    update_advisor_summary()