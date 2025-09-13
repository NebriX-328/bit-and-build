from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'funds', views.FundSourceViewSet, basename='fundsource')
router.register(r'allocations', views.AllocationViewSet, basename='allocation')
router.register(r'proofs', views.ProofViewSet, basename='proof')
router.register(r'feedback', views.FeedbackViewSet, basename='feedback')

urlpatterns = [
    path('', include(router.urls)),
    path('chatbot/', views.chatbot_query, name='chatbot'),
]
