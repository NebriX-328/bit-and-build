import hashlib
from PIL import Image
import google.generativeai as genai
from django.conf import settings
from rest_framework import viewsets, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from .models import FundSource, Allocation, Proof, Feedback, User
from .serializers import FundSourceSerializer, AllocationSerializer, ProofSerializer, FeedbackSerializer

class FundSourceViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Admins to manage Fund Sources.
    """
    queryset = FundSource.objects.all().order_by('-created_at')
    serializer_class = FundSourceSerializer
    permission_classes = [permissions.IsAdminUser]

    # ADD THIS NEW ACTION
    @action(detail=True, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def generate_summary(self, request, pk=None):
        """
        An action to generate a natural language summary of how a fund has been spent,
        using the Gemini AI.
        """
        try:
            fund_source = self.get_object()
            
            # --- Gather all related data for this fund ---
            allocations = Allocation.objects.filter(fund_source=fund_source)
            if not allocations.exists():
                return Response({"summary": "This fund has no allocations yet."})

            context_data = f"Here is the spending data for the fund '{fund_source.source_name}', which has a total budget of {fund_source.total_amount} INR:\n"
            
            for alloc in allocations:
                context_data += f"- Project: '{alloc.project_name}' was allocated {alloc.allocated_amount} INR. "
                proofs = Proof.objects.filter(allocation=alloc)
                if proofs.exists():
                    proof_statuses = ", ".join([proof.get_status_display() for proof in proofs])
                    context_data += f"It has {proofs.count()} proof(s) with statuses: {proof_statuses}.\n"
                else:
                    context_data += "It has no proofs submitted yet.\n"

            # --- Create the prompt for the AI ---
            prompt = f"""
            You are a financial analyst summarizing spending for a public transparency report.
            Based ONLY on the data below, write a brief, easy-to-understand paragraph (3-4 sentences) that summarizes how the fund's money has been allocated and the status of the projects.
            Start the summary with "Here is a summary for the '{fund_source.source_name}' fund:".

            --- DATA ---
            {context_data}
            --------------

            SUMMARY:
            """

            # --- Call the Gemini API ---
            genai.configure(api_key=settings.GEMINI_API_KEY)
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(prompt)

            return Response({"summary": response.text})

        except Exception as e:
            return Response({"error": f"An error occurred during summary generation: {e}"}, status=500)


class AllocationViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Admins to manage Allocations.
    Supports filtering by fund_source and receiver.
    """
    queryset = Allocation.objects.all().order_by('-created_at')
    serializer_class = AllocationSerializer
    permission_classes = [permissions.IsAdminUser]
    filterset_fields = ['fund_source', 'receiver']

class ProofViewSet(viewsets.ModelViewSet):
    """
    API endpoint for users to submit Proofs and for Admins to manage them.
    Supports filtering by allocation and status.
    """
    queryset = Proof.objects.all().order_by('-upload_timestamp')
    serializer_class = ProofSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    filterset_fields = ['allocation', 'status']

    def perform_create(self, serializer):
        """
        Automatically calculates the SHA-256 hash of an uploaded file upon creation.
        """
        uploaded_file = serializer.validated_data.get('uploaded_file')
        if uploaded_file:
            hasher = hashlib.sha256()
            for chunk in uploaded_file.chunks():
                hasher.update(chunk)
            serializer.save(file_hash=hasher.hexdigest())
        else:
            serializer.save()

    @action(detail=True, methods=['get', 'post'], permission_classes=[permissions.IsAdminUser])
    def verify(self, request, pk=None):
        """
        Admin action to verify a proof, including a geo-location check.
        """
        if request.method == 'POST':
            proof = self.get_object()
            allocation = proof.allocation
            lat_diff = abs(proof.upload_location_lat - allocation.registered_location_lat)
            lon_diff = abs(proof.upload_location_lon - allocation.registered_location_lon)

            # Tolerance for location match (e.g., approx 11km)
            if lat_diff < 0.1 and lon_diff < 0.1:
                proof.status = Proof.Status.VERIFIED
            else:
                proof.status = Proof.Status.FLAGGED

            proof.save()
            serializer = self.get_serializer(proof)
            return Response(serializer.data)
        
        return Response({"message": "Use a POST request to confirm this action."})

    @action(detail=True, methods=['get', 'post'], permission_classes=[permissions.IsAdminUser])
    def flag(self, request, pk=None):
        """
        Admin action to manually flag a proof.
        """
        if request.method == 'POST':
            proof = self.get_object()
            proof.status = Proof.Status.FLAGGED
            proof.save()
            serializer = self.get_serializer(proof)
            return Response(serializer.data)
            
        return Response({"message": "Use a POST request to confirm this action."})

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def analyze_image(self, request, pk=None):
        """
        Admin action to analyze a proof's image using the Gemini Vision model.
        """
        try:
            proof = self.get_object()
            if not proof.uploaded_file:
                return Response({"error": "No file uploaded for this proof."}, status=400)

            genai.configure(api_key=settings.GEMINI_API_KEY)
            model = genai.GenerativeModel('gemini-1.5-flash')
            image_file = Image.open(proof.uploaded_file)
            
            prompt = """
            Analyze this image and provide a brief, one-paragraph summary.
            Does it appear to be a valid financial document like a receipt or invoice?
            If so, what is the total amount visible?
            """

            response = model.generate_content([prompt, image_file])
            return Response({"analysis": response.text})

        except Exception as e:
            return Response({"error": f"An error occurred during analysis: {e}"}, status=500)

class FeedbackViewSet(viewsets.ModelViewSet):
    """
    API endpoint for users to submit feedback on allocations.
    Supports filtering by allocation and user.
    """
    queryset = Feedback.objects.all().order_by('-created_at')
    serializer_class = FeedbackSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]
    filterset_fields = ['allocation', 'user']

    def perform_create(self, serializer):
        """
        Automatically associates feedback with the logged-in user.
        """
        serializer.save(user=self.request.user)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def chatbot_query(request):
    """
    An AI-powered chatbot that uses the Gemini API to answer user queries
    based on the current state of the database.
    """
    genai.configure(api_key=settings.GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')

    user_query = request.data.get('query', '')
    if not user_query:
        return Response({"answer": "Please ask a question."}, status=400)

    allocations = Allocation.objects.select_related('fund_source', 'receiver').all()
    
    context_data = "Here is the current financial data:\n"
    for alloc in allocations:
        context_data += f"- Project: '{alloc.project_name}', "
        context_data += f"Amount: {alloc.allocated_amount} INR, "
        context_data += f"Allocated to: {alloc.receiver.username}, "
        context_data += f"From Fund: '{alloc.fund_source.source_name}'.\n"

    prompt = f"""
    You are a helpful assistant for a financial transparency application.
    Based ONLY on the data provided below, answer the user's question in a concise, friendly manner.
    Do not use any external knowledge. If the data doesn't contain the answer, say that you cannot find that information in the records.

    --- DATA ---
    {context_data}
    --------------

    USER'S QUESTION: "{user_query}"

    ANSWER:
    """

    try:
        response = model.generate_content(prompt)
        answer = response.text
    except Exception as e:
        answer = f"Sorry, there was an error processing your request: {e}"

    return Response({"answer": answer})
