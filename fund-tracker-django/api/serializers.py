# api/serializers.py

from rest_framework import serializers
from .models import User, FundSource, Allocation, Proof, Feedback
from django.db.models import Sum 
from django.conf import settings

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']

class FundSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = FundSource
        fields = '__all__'
        depth = 1
    
    def get_total_amount_display(self, obj):
        # Check the request context for a currency query parameter
        request = self.context.get('request')
        if request and request.query_params.get('currency') == 'USD':
            amount = obj.total_amount / settings.USD_TO_INR_RATE
            return f"${amount:,.2f} USD" # Format as $1,234.56 USD
        
        return f"₹{obj.total_amount:,.2f} INR" # Default to INR
        

class AllocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Allocation
        fields = '__all__'
        depth = 1

    def get_allocated_amount_display(self, obj):
        request = self.context.get('request')
        if request and request.query_params.get('currency') == 'USD':
            amount = obj.allocated_amount / settings.USD_TO_INR_RATE
            return f"${amount:,.2f} USD"
        
        return f"₹{obj.allocated_amount:,.2f} INR"
    
    def validate(self, data):
        """
        Check that the allocation does not exceed the fund source's total budget.
        """
        fund_source = data['fund_source']
        new_allocation_amount = data['allocated_amount']
        
        existing_allocations_sum = Allocation.objects.filter(fund_source=fund_source).aggregate(total=Sum('allocated_amount'))['total'] or 0

        if self.instance:
            existing_allocations_sum -= self.instance.allocated_amount

        if existing_allocations_sum + new_allocation_amount > fund_source.total_amount:
            raise serializers.ValidationError(f"This allocation exceeds the budget. The '{fund_source.source_name}' fund only has ${fund_source.total_amount - existing_allocations_sum} remaining.")
        
        return data

class ProofSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proof
        fields = '__all__'
        read_only_fields = ['file_hash', 'status']
        depth = 1


class FeedbackSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Feedback
        fields = ['id', 'allocation', 'user', 'comment', 'image', 'created_at']
