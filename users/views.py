from datetime import timedelta
from django.utils import timezone
from django.shortcuts import render
#from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import renderers
from rest_framework import generics
from rest_framework_simplejwt.views import TokenObtainPairView
import shortuuid
from rest_framework.response import Response
from rest_framework import status
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.http import Http404
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import logging
from users.models import User, UserProfile
from users.serializer import MyTokenObtainPairSerializer, RegisterSerializer, UserSerializer


class MyTokenObtainPairView(TokenObtainPairView):
        serializer_class = MyTokenObtainPairSerializer
        
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

def generate_otp():
     uuid_key = shortuuid.uuid()
     otp = uuid_key[:6]
     return otp



logger = logging.getLogger(__name__)
def send_otp_email(email, otp, reset_link=None):
    """
    Send OTP email with HTML template and fallback to text version.
    
    Args:
        email (str): Recipient email address
        otp (str): The OTP code
        reset_link (str, optional): Password reset link. Defaults to None.
    
    Returns:
        bool: True if email was sent successfully, False otherwise
    """
    subject = 'Password Reset Email'
    
    # Render HTML template
    context = {
        'otp': otp,
        'reset_link': reset_link or 'Not available',
    }
    
    try:
        html_content = render_to_string('emails/password_reset_email.html', context)
        text_content = strip_tags(html_content)  # Fallback text version
        
        msg = EmailMultiAlternatives(
            subject,
            text_content,
            settings.EMAIL_HOST_USER,
            [email]
        )
        msg.attach_alternative(html_content, "text/html")
        
        msg.send()
        logger.info(f"Password reset email sent successfully to {email}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send password reset email to {email}: {str(e)}")
        return False



#Password Reset
class PasswordResetEmailVerify(generics.RetrieveAPIView): 
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def get_object(self):
        email = self.kwargs['email']
        try:
            user = User.objects.get(email=email)
            
            otp = generate_otp()
            user.otp_created_at = timezone.now()
            user.otp = otp
            user.save()

            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            otp = user.otp

            reset_link = f"http://localhost:8000/api/user/password-reset-confirm?token={otp}&uidb64={uidb64}"
            
            # Send email with error handling
            email_sent = send_otp_email(user.email, otp, reset_link)
            
            if not email_sent:
                logger.warning(f"Password reset email failed to send for user {user.email}")
                # You might want to implement retry logic here or notify admins
            
            return user
            
        except User.DoesNotExist:
            logger.warning(f"Password reset requested for non-existent email: {email}")
            raise Http404("User with this email does not exist.")
        except Exception as e:
            logger.error(f"Error in password reset for email {email}: {str(e)}")
            raise Http404("An error occurred while processing your request.")


#Password Change
#logger = logging.getLogger(__name__)
class PasswordChangeView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        payload = request.data
        otp = payload.get('otp')
        uidb64 = payload.get('uidb64')
        new_password = payload.get('new_password')

        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))            
            user = User.objects.get(pk=user_id)
            
            # Check if OTP matches and is not expired
            if not self.is_valid_otp(user, otp):
                return Response(
                    {"error": "Invalid or expired OTP"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Change password and clear OTP
            user.set_password(new_password)
            user.otp = None
            user.otp_created_at = None 
            user.save()
            
            return Response(
                {"message": "Password changed successfully"}, 
                status=status.HTTP_200_OK
            )

        except (TypeError, ValueError, OverflowError):
            logger.warning(f"Invalid base64 uid received: {uidb64}")
            return Response(
                {"error": "Invalid reset link"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        except User.DoesNotExist:
            logger.warning(f"Password change failed for invalid user ID: {user_id}")
            return Response(
                {"error": "Invalid user"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        except Exception as e:
            logger.error(f"Password change error: {str(e)}")
            return Response(
                {"error": "Internal server error"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def is_valid_otp(self, user, otp):
        """Check if OTP is valid and not expired"""
        if not user.otp or user.otp != otp:
            return False
            
        if not user.otp_created_at:
            logger.warning(f"OTP without timestamp for user {user.id}")
            return False
            
        expiration_time = user.otp_created_at + timedelta(minutes=15)
        if timezone.now() > expiration_time:
            return False
            
        return True