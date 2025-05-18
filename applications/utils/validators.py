from django.conf import settings
from django.core.exceptions import ValidationError
import magic

def validate_file_type(file):
    """
    Validate that the uploaded file is of an allowed type.
    """
    file_mime = magic.from_buffer(file.read(1024), mime=True)
    file.seek(0)  # Reset file pointer
    
    if file_mime not in settings.DOCUMENT_ALLOWED_TYPES:
        raise ValidationError('Unsupported file type. Please upload PDF, Word, or image files.')

def validate_file_size(file):
    """
    Validate that the uploaded file is within size limits.
    """
    if file.size > settings.DOCUMENT_MAX_SIZE:
        raise ValidationError('The file size is too large. Maximum size allowed is 5MB.')