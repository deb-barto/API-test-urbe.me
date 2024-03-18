import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from datacontrol.models import ClientSummary, Transaction

def populate():
    with open('clients.json', 'r') as file:
        clientes = json.load(file)
        for cliente in clientes:
            # Criando o objeto ClientSummary
            client_obj = ClientSummary.objects.create(
                name=cliente['name'],
                broker=cliente['broker']
            )
            # Supondo que o JSON foi corrigido para usar 'name' e 'broker'
            # ou mude para cliente['nome'], cliente['corretora'] se o seu JSON ainda usa essas chaves

            # Iterando pelas transações de cada cliente
            for transaction in cliente.get('transactions', []):  # Usando .get para evitar KeyError se não houver transações
                Transaction.objects.create(
                    client=client_obj,
                    date=transaction['date'],
                    value=transaction['value'],
                    transaction_type=transaction['transaction_type']
                )

if __name__ == '__main__':
    print("Populando o banco de dados...")
    populate()
    print("População completa!")