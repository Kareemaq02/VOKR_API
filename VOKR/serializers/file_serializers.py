from rest_framework import serializers

class FileUploadSerializer(serializers.Serializer):
    company_name = serializers.CharField(max_length=255, required=True)
    file = serializers.FileField(required=True)
