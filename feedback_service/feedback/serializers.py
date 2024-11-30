import uuid
from rest_framework import serializers
from .models import Feedback

class FeedbackSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    timestamp = serializers.CharField()

    class Meta:
        model = Feedback
        fields = ['id', 'customer_id', 'feedback_text', 'timestamp']

    def create(self, validated_data):
        validated_data['id'] = str(uuid.uuid4())
        return super().create(validated_data)
