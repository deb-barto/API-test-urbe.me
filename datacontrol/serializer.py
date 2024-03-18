from rest_framework import serializers
from datacontrol.models import AdvisorSummary, ClientSummary, Transaction

class AdvisorSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvisorSummary
        fields = ['total_equity', 'average_equity', 'total_clients']


class TransactionSerializer(serializers.ModelSerializer):
    client = serializers.PrimaryKeyRelatedField(read_only=True)  
    class Meta:
        model = Transaction
        fields = ['id', 'client', 'date', 'value', 'transaction_type']
        read_only_fields = ('client',)

    def create(self, validated_data):
        client_id = self.context['view'].kwargs.get('client_id')
        client = ClientSummary.objects.get(id=client_id)
        validated_data.pop('client', None) 
        return Transaction.objects.create(client=client, **validated_data)

class ClientSummarySerializer(serializers.ModelSerializer):
    transactions = TransactionSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = ClientSummary
        fields = ['id', 'name', 'broker','transactions','total']

    def get_total(self, obj):
        return obj.calculate_total()