import time
import random 
from celery import shared_task 
from .models import Attachment 

@shared_task
def process_attachment(attachment_id):
    try:
        attachment = Attachment.objects.get(id=attachment_id)

        #updating status to processing 
        attachment.status = 'processing'
        attachment.save()

        # mock wait (2-5 second)
        time.sleep(random.randint(2,5))

        #mock data
        mockdata = generate_mock_data(attachment.file_type)
        attachment.transcript = mockdata['transcript']
        attachment.summary = mockdata['summary']
        attachment.status = 'done'
        attachment.save()

        print(f"Processed attachment {attachment.id} successfully")

        # Mock email notification
        print(f"Email notification: Your {attachment.file_type} file has been processed!")
        
        return f"Successfully processed attachment {attachment_id}"
    except Attachment.DoesNotExist:
        return f"Attachment {attachment_id} not found"
    except Exception as e:
        # Mark as failed if something goes wrong
        if 'attachment' in locals():
            attachment.status = 'failed'
            attachment.save()
        return f"Error processing attachment {attachment_id}: {str(e)}"

def generate_mock_data(file_type):
    mock_content = {
        'audio': {
            'transcript': "This is a mock transcript for an audio file. The speaker discussed knowledge transfer processes, best practices, and team collaboration strategies. Key points included documentation standards, communication protocols, and knowledge retention techniques.",
            'summary': "Audio session covering KT processes, documentation standards, and team collaboration best practices."
        },
        'video': {
            'transcript': "Mock video transcript: This presentation covers the fundamentals of knowledge transfer in software development. Topics include code reviews, pair programming, technical documentation, and onboarding processes for new team members.",
            'summary': "Video presentation on software development knowledge transfer fundamentals and team onboarding."
        },
        'pdf': {
            'transcript': "Mock PDF content: This document outlines the knowledge transfer framework including process documentation, training materials, and assessment criteria. It covers both technical and soft skills transfer methodologies.",
            'summary': "PDF document detailing knowledge transfer framework and methodologies for technical teams."
        },
        'text': {
            'transcript': "Mock text file content: Knowledge transfer session notes including discussion points, action items, and follow-up tasks. The session covered project handover procedures and documentation requirements.",
            'summary': "Text notes from KT session covering project handover procedures and documentation requirements."
        }
    }
    
    return mock_content.get(file_type, {
        'transcript': "Mock transcript content for uploaded file.",
        'summary': "Mock summary of the uploaded content."
    })


