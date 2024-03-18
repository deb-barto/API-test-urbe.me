from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from datacontrol.views import AdvisorSummaryView, ClientSummaryViewSet,TransactionViewSet

router = DefaultRouter()
router.register(r'clients', ClientSummaryViewSet, basename='clients')
router.register(r'transactions', TransactionViewSet, basename='transactions')

urlpatterns = [

    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('advisor_summary/', AdvisorSummaryView.as_view(), name='advisor-summary'),
    path('', include(router.urls)),
     path('client/<int:client_id>/transaction/', include([
        path('', TransactionViewSet.as_view({'get': 'list', 'post': 'create'}), name='client-transaction-list'),
        path('<int:pk>/', TransactionViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'update', 'delete': 'destroy'}), name='client-transaction-detail'),
    ])),
]