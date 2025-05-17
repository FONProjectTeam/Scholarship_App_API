from django.urls import path
from users import views as users_views

urlpatterns = [
    path('user/register/', users_views.RegisterView.as_view(), name='register'),
    path('user/token/', users_views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('user/password-reset/<email>/', users_views.PasswordResetEmailVerify.as_view(), name='password-reset'),
    path('user/password-change/', users_views.PasswordResetEmailVerify.as_view(), name='password-change'),
    #path('profile/', users_views.UserProfileView.as_view(), name='user_profile'),
    #path('profile/update/', users_views.UpdateUserProfileView.as_view(), name='update_user_profile'),
]