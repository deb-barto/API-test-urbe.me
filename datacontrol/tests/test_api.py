from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from datacontrol.models import AdvisorSummary, ClientSummary, Transaction
from datetime import date
from django.contrib.auth.models import User

class ClientAPITests(APITestCase):

    def setUp(self):
        self.test_client = ClientSummary.objects.create(name="Test Client", broker="A")
        self.create_url = reverse('clients-list')
        self.detail_url = reverse('clients-detail', kwargs={'pk': self.test_client.pk})

    def test_create_client(self):
        data = {'name': 'New Client', 'broker': 'B'}
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ClientSummary.objects.count(), 2)  # Incluindo o criado em setUp
        self.assertEqual(ClientSummary.objects.latest('id').name, 'New Client')

    def test_delete_client(self):
        response = self.client.delete(self.detail_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ClientSummary.objects.count(), 0) 

    def test_update_client(self):
        updated_data = {'name': 'Updated Client', 'broker': 'C'}
        response = self.client.put(self.detail_url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.test_client.refresh_from_db()  # Atualiza o objeto com os valores do banco
        self.assertEqual(self.test_client.name, 'Updated Client')
        self.assertEqual(self.test_client.broker, 'C')

class ClientTransactionAPITests(APITestCase):

    def setUp(self):
        self.client_summary = ClientSummary.objects.create(name='Test Client', broker='A')

    def test_register_transaction(self):
        url = reverse('client-transaction-list', kwargs={'client_id': self.client_summary.id})
        data = {
            'date': '2024-01-01',
            'value': 1000.00,
            'transaction_type': 'Aporte',
        }
        response = self.client.post(url, data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Transaction.objects.count(), 1)
        transaction = Transaction.objects.first()
        self.assertEqual(transaction.client.id, self.client_summary.id)
        self.assertEqual(transaction.value, 1000.00)
        self.assertEqual(transaction.transaction_type, 'Aporte')