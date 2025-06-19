from rest_framework import serializers 
from .models import KTSession , Attachment 


class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = [
            'id', 'file_type', 'file_url', 'status', 
            'transcript', 'summary', 'created_at'
        ]
        read_only_fields = ['id', 'file_url', 'status', 'transcript', 'summary', 'created_at']

class KTSessionSerializer(serializers.ModelSerializer):
    attachments = AttachmentSerializer(many=True, read_only=True)
    created_by_name = serializers.CharField(source='created_by.name', read_only=True)
    share_url = serializers.SerializerMethodField()
    
    class Meta:
        model = KTSession
        fields = [
            'id', 'title', 'description', 'created_by', 'created_by_name',
            'share_token', 'share_url', 'attachments', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_by', 'share_token', 'created_at', 'updated_at']
    
    def get_share_url(self, obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(f'/api/sessions/shared/{obj.share_token}/')
        return f'/api/sessions/shared/{obj.share_token}/'

class KTSessionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = KTSession
        fields = ['title', 'description']

class PublicKTSessionSerializer(serializers.ModelSerializer):
    attachments = AttachmentSerializer(many=True, read_only=True)
    created_by_name = serializers.CharField(source='created_by.name', read_only=True)
    
    class Meta:
        model = KTSession
        fields = [
            'id', 'title', 'description', 'created_by_name',
            'attachments', 'created_at'
        ]