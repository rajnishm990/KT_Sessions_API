from rest_framework import status , viewsets 
from rest_framework.decorators import action , api_view , permission_classes 
from rest_framework.permissions import AllowAny, IsAuthenticated 
from rest_framework.response import Response
from django.shortcuts import get_object_or_404 
from django.http import Http404 

from .models import KTSession , Attachment 
from .serializers import (
    KTSessionSerializer, KTSessionCreateSerializer, 
    AttachmentSerializer, PublicKTSessionSerializer
)
from .tasks import process_attachment 

class KTSessionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action =='create':
            return KTSessionCreateSerializer 
        return KTSessionSerializer 
    
    def get_queryset(self):
        return KTSession.objects.filter(created_by = self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=True , methods=['post'])
    def add_attachment(self,request, pk=None):
        session = self.get_object()

        #user should own this session for adding attachment
        if session.created_by != request.user:
            return Response(
                {'error': 'You can only add attachments to your own sessions'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = AttachmentSerializer(data=request.data) 
        if serializer.is_valid():
            attachment = serializer.save(session=session)

            # queue the attachment to be processed 
            process_attachment.delay(str(attachment.id))

            return Response(serializer.data , status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])
def shared_session_view(request, share_token):
    try:
        session = KTSession.objects.get(share_token=share_token)
        serializer = PublicKTSessionSerializer(session, context={'request': request})
        return Response(serializer.data)
    except KTSession.DoesNotExist:
        return Response(
            {'error': 'Session not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def attachment_detail(request, attachment_id):
    try:
        attachment = Attachment.objects.get(id=attachment_id)
        
        # Check if user owns the session this attachment belongs to
        if attachment.session.created_by != request.user:
            return Response(
                {'error': 'You can only access attachments from your own sessions'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        if request.method == 'GET':
            serializer = AttachmentSerializer(attachment)
            return Response(serializer.data)
        
        elif request.method == 'PUT':
            serializer = AttachmentSerializer(attachment, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        elif request.method == 'DELETE':
            attachment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    
    except Attachment.DoesNotExist:
        return Response(
            {'error': 'Attachment not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )


