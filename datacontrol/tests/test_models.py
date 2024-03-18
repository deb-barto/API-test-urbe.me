
from django.test import TestCase
from datacontrol.models import ClientSummary, Transaction, AdvisorSummary
from datetime import date

class ModelsTestCase(TestCase):

    def setUp(self):
        self.client_summary = ClientSummary.objects.create(name="Client 1", broker="A")
        Transaction.objects.create(client=self.client_summary, date=date.today(), value=1000.00, transaction_type="Aporte")
        Transaction.objects.create(client=self.client_summary, date=date.today(), value=500.00, transaction_type="Resgate")


    def test_transaction_total(self):
        total = self.client_summary.calculate_total()
        self.assertEqual(total, 500.00) 

    def test_advisor_summary_update(self):
        advisor_summary = AdvisorSummary.objects.first()
        
        self.assertIsNotNone(advisor_summary)
        self.assertEqual(advisor_summary.total_equity, 500.00)
        self.assertEqual(advisor_summary.average_equity, 500.00) 
        self.assertEqual(advisor_summary.total_clients, 1)
        
        Transaction.objects.create(client=self.client_summary, date=date.today(), value=1000.00, transaction_type="Aporte")
        advisor_summary.refresh_from_db()
        self.assertEqual(advisor_summary.total_equity, 1500.00)
        self.assertEqual(advisor_summary.average_equity, 1500.00) 

    def test_advisor_summary_with_multiple_clients(self):
        ClientSummary.objects.create(name="Client 2", broker="B")
        advisor_summary = AdvisorSummary.objects.first()
        advisor_summary.refresh_from_db()
        self.assertEqual(advisor_summary.total_clients, 2)
        self.assertEqual(advisor_summary.average_equity, advisor_summary.total_equity / 2)