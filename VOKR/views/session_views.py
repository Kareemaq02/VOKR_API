from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.utils import timezone
from ..models import Session, Message, Company, File
import uuid
import requests
from ..services.semantic_search import SemanticSearch

class CreateNewSessionView(APIView):
    def post(self, request):
        # Generate a unique session ID
        session_id = f"session_{uuid.uuid4()}"
        
        # Start a transaction to handle both session creation and initial message insertion
        try:
            with transaction.atomic():
                # Create a new session in the Session table
                session = Session.objects.create(session_id=session_id, created_at=timezone.now())
                
                # Create the initial message in the Messages table
                initial_message_content = "Hello! I'm here to help you. How can I assist you today?"
                initial_message = Message.objects.create(
                    session=session,
                    role=Message.ASSISTANT_ROLE,
                    message=initial_message_content,
                    sent_timestamp=timezone.now()
                )

                # Fetch all messages related to this session to include in the response
                messages = Message.objects.filter(session=session).values('role', 'message', 'sent_timestamp')

                # Return the session ID and its messages
                return Response({
                    "session_id": session_id,
                    "messages": list(messages)
                }, status=status.HTTP_201_CREATED)

        except Exception as e:
            # Handle any exceptions by returning an error response
            return Response({
                "error": "An error occurred while creating the session and initial message.",
                "details": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
class SendMessageView(APIView):
    def post(self, request, session_id):
        # Get the user's message and access key from the request
        user_message_content = request.data.get('message')
        access_key = request.data.get('access_key')

        if not user_message_content:
            return Response({"error": "Message content is required."}, status=status.HTTP_400_BAD_REQUEST)
        if not access_key:
            return Response({"error": "Access key is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Start a database transaction
            with transaction.atomic():
                       
                # Retrieve the company using the provided access key
                company = Company.objects.filter(access_key=access_key).first()

                if not company:
                    return Response({"error": "Invalid access key."}, status=status.HTTP_400_BAD_REQUEST)

                # Retrieve the company ID
                company_id = company.pk

                # Retrieve the file associated with the company ID
                company_file = File.objects.filter(company_id=company_id).first()

                if not company_file:
                    return Response({"error": "No manual file found for this company."}, status=status.HTTP_400_BAD_REQUEST)

                # Perform semantic search to get the extracted answer
                semantic_search = SemanticSearch(company_file.file_path)
                extracted_answer = semantic_search.search_manual(user_message_content)
                
                # Fetch the session and update its last accessed time
                session = Session.objects.select_for_update().get(session_id=session_id)
                session.last_accessed_at = timezone.now()
                session.save()

                # Fetch all previous messages related to this session, ordered by sent_at
                previous_messages = Message.objects.filter(session=session).order_by('sent_timestamp')

                # Build the messages list for the chat API, including previous messages
                messages = []
                for msg in previous_messages:
                    messages.append({
                        "role": msg.role,
                        "content": msg.message
                    })

                # Create the refined prompt for the assistant
                prompt = f"""You are working at customer support. Refine it and simplify it and instantly reply without explaining to me that you are an AI and that you are doing this as an answer for what I said above just give me the refined answer without such answers as: "Here is your answer:" or whatever. If the answer was "No relevant information found in the manual", then just explain that you have no idea and ask them to contact the company. Here is the question you are being asked: {user_message_content}, and here is its answer: {extracted_answer}. Answer instantly without sentences similar to "Sure, I'd be happy to help! Here is your refined answer:" or "Of course! Here is your answer:" just place the answer directly"""

                # Append the prompt as the last message in the messages list
                messages.append({
                    "role": Message.USER_ROLE,
                    "content": prompt
                })

                # Send the prompt to the chat API
                chat_api_url = "http://localhost:11434/api/chat"
                payload = {
                    "model": "llama3.1",
                    "messages": messages,
                    "stream": False
                }

                # Make the API request
                response = requests.post(chat_api_url, json=payload)
                if response.status_code != 200:
                    return Response({
                        "error": "Failed to get response from chat API.",
                        "details": response.text
                    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                # Parse the assistant's response
                response_data = response.json()
                assistant_message_content = response_data.get("message", {}).get("content", "Sorry, I couldn't understand that.")

                # Add the original user's message to the Message table
                user_message = Message.objects.create(
                    session=session,
                    role=Message.USER_ROLE,
                    message=user_message_content  # Store the original question here
                )
                
                # Add the assistant's response to the Message table
                assistant_message = Message.objects.create(
                    session=session,
                    role=Message.ASSISTANT_ROLE,
                    message=assistant_message_content
                )

                # Return the session details along with the messages
                messages = Message.objects.filter(session=session).order_by('sent_timestamp')
                message_data = [{"role": msg.role, "message": msg.message, "sent_timestamp": msg.sent_timestamp} for msg in messages]

                return Response({
                    "session_id": session.session_id,
                    "messages": message_data,
                    "last_accessed_at": session.last_accessed_at
                }, status=status.HTTP_200_OK)

        except Session.DoesNotExist:
            return Response({"error": "Session not found."}, status=status.HTTP_404_NOT_FOUND)
        except requests.exceptions.RequestException as e:
            return Response({"error": f"API request failed: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

