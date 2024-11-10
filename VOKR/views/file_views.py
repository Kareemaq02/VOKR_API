import os
import mimetypes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Company, File
from ..serializers.file_serializers import FileUploadSerializer
from django.utils import timezone
from django.db import IntegrityError, DatabaseError

class FileUploadView(APIView):
    def post(self, request):
        try:
            serializer = FileUploadSerializer(data=request.data)
            if serializer.is_valid():
                company_name = serializer.validated_data['company_name']

                # Check if company exists or create a new one
                try:
                    company, created = Company.objects.get_or_create(name=company_name)
                except IntegrityError:
                    return Response({'error': 'Database integrity error while creating company.'},
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                except DatabaseError:
                    return Response({'error': 'A database error occurred.'},
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                # Define the directory path
                base_dir = os.path.join('C:\\', 'vokr_documents')
                company_dir = os.path.join(base_dir, company_name)

                # Create the company's folder if it doesn't exist
                if not os.path.exists(company_dir):
                    try:
                        os.makedirs(company_dir)
                    except OSError as e:
                        return Response({'error': f'Failed to create directory: {str(e)}'},
                                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                # Save the file in the directory
                uploaded_file = serializer.validated_data['file']
                file_path = os.path.join(company_dir, uploaded_file.name)

                # Check if a file with the same name already exists
                if os.path.exists(file_path):
                    return Response({'error': 'A file with the same name already exists.'},
                                    status=status.HTTP_409_CONFLICT)

                # Extract file type using mimetypes or file extension
                file_type, _ = mimetypes.guess_type(file_path)
                if not file_type:
                    file_type = uploaded_file.name.split('.')[-1] if '.' in uploaded_file.name else 'unknown'

                # Extract base file name without extension
                base_file_name = os.path.splitext(uploaded_file.name)[0]

                try:
                    with open(file_path, 'wb+') as destination:
                        for chunk in uploaded_file.chunks():
                            destination.write(chunk)
                except IOError as e:
                    return Response({'error': f'Failed to save file: {str(e)}'},
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                # Save file details to the database
                try:
                    File.objects.create(
                        file_name=base_file_name,  # Save only the base name
                        file_type=file_type,
                        uploaded_at=timezone.now(),
                        file_path=file_path,
                        company_id=company.id
                    )
                except DatabaseError:
                    return Response({'error': 'A database error occurred while saving file details.'},
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                return Response({'message': 'File uploaded successfully.'}, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            # Catch any other unexpected errors
            return Response({'error': f'An unexpected error occurred: {str(e)}'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
