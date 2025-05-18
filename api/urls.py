from django.urls import path, include
from users import views as users_views

from rest_framework.routers import DefaultRouter

#from .api.auth.views import UserRegistrationView, UserLoginView
from users.views import UserProfileViewSet
from scholarships.views import ScholarshipViewSet, ScholarshipCategoryViewSet
from applications.views import ApplicationViewSet, DocumentViewSet
from reviews.views import ReviewViewSet
from notifications.views import NotificationViewSet, NotificationPreferenceViewSet

router = DefaultRouter()
router.register(r'profiles', UserProfileViewSet, basename='profile')
router.register(r'scholarships', ScholarshipViewSet, basename='scholarship')
router.register(r'categories', ScholarshipCategoryViewSet, basename='category')
router.register(r'applications', ApplicationViewSet, basename='application')
router.register(r'documents', DocumentViewSet, basename='document')
router.register(r'reviews', ReviewViewSet, basename='review')
router.register(r'notifications', NotificationViewSet, basename='notification')
router.register(r'notification-preferences', NotificationPreferenceViewSet, basename='notification-preference')


urlpatterns = [

    path('user/register/', users_views.RegisterView.as_view(), name='register'),
    path('user/token/', users_views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('user/password-reset/<email>/', users_views.PasswordResetEmailVerify.as_view(), name='password-reset'),
    path('user/password-change/', users_views.PasswordChangeView.as_view(), name='password-change'),
    # API endpoints for user authentication and registration
    path('', include(router.urls)),
    
    #path('user/profile/', users_views.UserProfileView.as_view(), name='user_profile'),
]