from rest_framework import status, views, viewsets, mixins
from rest_framework.response import Response
from .models import AdvisorSummary, ClientSummary, Transaction
from .serializer import AdvisorSummarySerializer, ClientSummarySerializer, TransactionSerializer

class AdvisorSummaryView(views.APIView):
    def get(self, request, *args, **kwargs):
        advisor_summary = AdvisorSummary.objects.first()
        if advisor_summary:
            serializer = AdvisorSummarySerializer(advisor_summary)
            return Response(serializer.data)
        return Response({"message": "Advisor summary not found."}, status=status.HTTP_404_NOT_FOUND)

class ClientSummaryViewSet(viewsets.ModelViewSet):
    queryset = ClientSummary.objects.all()
    serializer_class = ClientSummarySerializer

class TransactionViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    serializer_class = TransactionSerializer
    def get_serializer_context(self):
        context = super(TransactionViewSet, self).get_serializer_context()
        context.update({
            'client_id': self.kwargs.get('client_id')
        })
        return context
    def get_queryset(self):
        client_id = self.kwargs.get('client_id')
        if client_id is not None:
            return Transaction.objects.filter(client__id=client_id)
        return Transaction.objects.all()

    def perform_create(self, serializer):
        client_id = self.kwargs.get('client_id')
        client = ClientSummary.objects.get(id=client_id)
        serializer.save(client=client)