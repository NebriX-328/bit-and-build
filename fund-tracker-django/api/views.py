# api/views.py

from rest_framework import viewsets, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from .models import FundSource, Allocation, Proof
from .serializers import FundSourceSerializer, AllocationSerializer, ProofSerializer

class FundSourceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows fund sources to be viewed or edited.
    """
    queryset = FundSource.objects.all().order_by('-created_at')
    serializer_class = FundSourceSerializer
    # CHANGE THIS LINE
    permission_classes = [permissions.IsAdminUser]

class AllocationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows allocations to be viewed or edited.
    """
    queryset = Allocation.objects.all().order_by('-created_at')
    serializer_class = AllocationSerializer
    # CHANGE THIS LINE
    permission_classes = [permissions.IsAdminUser]

# The ProofViewSet remains the same and is correct
class ProofViewSet(viewsets.ModelViewSet):
    queryset = Proof.objects.all().order_by('-upload_timestamp')
    serializer_class = ProofSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]