# api/serializers.py

from rest_framework import serializers
from .models import User, FundSource, Allocation, Proof

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']

class FundSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = FundSource
        fields = '__all__' # This includes all fields from the model

class AllocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Allocation
        fields = '__all__'

class ProofSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proof
        fields = '__all__'