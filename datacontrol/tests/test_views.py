from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from datacontrol.models import ClientSummary, Transaction, AdvisorSummary
from datetime import date

class AdvisorSummaryViewTests(APITestCase):
    def setUp(self):
        AdvisorSummary.objects.get_or_create(
            total_equity=0.0, 
            average_equity=0.0, 
            total_clients=0
        )

    def test_get_advisor_summary(self):
        url = reverse('advisor-summary')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
      
class ClientSummaryViewSetTests(APITestCase):
    def setUp(self):
        self.client_summary = ClientSummary.objects.create(name="Client Test", broker="A")
        self.list_url = reverse('clients-list')
        self.detail_url = reverse('clients-detail', kwargs={'pk': self.client_summary.pk})

    def test_create_client(self):
        data = {'name': 'New Client', 'broker': 'B'}
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ClientSummary.objects.count(), 2) 

    def test_get_client(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.client_summary.name)

    def test_update_client(self):
        data = {'name': 'Updated Client', 'broker': 'B'}
        response = self.client.put(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client_summary.refresh_from_db()
        self.assertEqual(self.client_summary.name, 'Updated Client')

    def test_delete_client(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ClientSummary.objects.count(), 0)

class TransactionViewSetTests(APITestCase):
    def setUp(self):
        self.client_summary = ClientSummary.objects.create(name="Client Test", broker="A")
        self.transaction = Transaction.objects.create(client=self.client_summary, date=date.today(), value=500, transaction_type="Aporte")
        self.list_url = reverse('transactions-list')
        self.detail_url = reverse('transactions-detail', kwargs={'pk': self.transaction.pk})

    def test_get_transaction(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['value'], self.transaction.value)