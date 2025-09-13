# api/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'funds', views.FundSourceViewSet, basename='fundsource')
router.register(r'allocations', views.AllocationViewSet, basename='allocation')
router.register(r'proofs', views.ProofViewSet, basename='proof')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]