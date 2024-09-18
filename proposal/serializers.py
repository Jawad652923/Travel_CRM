from rest_framework import serializers
from .models import Proposals
from services.models import Service
from inquiries.models import Inquiries
from services.serializers import ServiceSerializer
from inquiries.serializers import InquirySerializer

class ProposalSerializer(serializers.ModelSerializer):
    services = serializers.PrimaryKeyRelatedField(queryset=Service.objects.all(), many=True)
    inquiry = serializers.PrimaryKeyRelatedField(queryset=Inquiries.objects.all())

    class Meta:
        model = Proposals
        fields = ['id', 'inquiry', 'details', 'services', 'status', 'cost']

    def create(self, validated_data):
        """
        Create a new Proposals instance.

        Args:
            validated_data (dict): A dictionary containing the validated data for the proposal. 
                                   This should include 'details', 'status', 'cost', and 'services'.

        Returns:
            Proposals: The created Proposals instance with associated services set.
        """
        services = validated_data.pop('services')
        proposal = Proposals.objects.create(**validated_data)
        proposal.services.set(services)
        return proposal

    def update(self, instance, validated_data):
        """
        Update an existing Proposals instance.

        Args:
            instance (Proposals): The Proposals instance to update.
            validated_data (dict): A dictionary containing the updated data. 
                                   This may include 'details', 'status', 'cost', 'inquiry', and 'services'.

        Returns:
            Proposals: The updated Proposals instance.
        """
        instance.details = validated_data.get('details', instance.details)
        instance.status = validated_data.get('status', instance.status)
        instance.cost = validated_data.get('cost', instance.cost)

        if 'inquiry' in validated_data:
            instance.inquiry = validated_data['inquiry']

        if 'services' in validated_data:
            instance.services.set(validated_data['services'])

        instance.save()
        return instance

    def to_representation(self, instance):
        """
        Convert the Proposals instance to a JSON-serializable format.

        Args:
            instance (Proposals): The Proposals instance to serialize.

        Returns:
            dict: A dictionary representing the serialized data, including detailed inquiry and services.
        """
        representation = super().to_representation(instance)
        representation['inquiry'] = InquirySerializer(instance.inquiry).data
        representation['services'] = ServiceSerializer(instance.services.all(), many=True).data
        return representation
