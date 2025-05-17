from django.contrib import admin
from users.models import User, UserProfile


class UserAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'email', 'user_type', 'phone_number', 'is_active')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    list_filter = ('user_type', 'is_active', 'is_staff')
    ordering = ('first_name', 'last_name') 
    list_editable = ('is_active',)
    
    def get_full_name(self, obj):
        return obj.get_full_name()
    get_full_name.short_description = 'Full Name'


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'user__email', 'education_level', 'major', 'graduation_year')
    search_fields = ('user__email', 'user__username', 'user__first_name', 'user__last_name', 'education_level', 'institution', 'major')
    list_filter = ('education_level', 'major', 'graduation_year')
    ordering = ('user__email',)

    def get_full_name(self, obj):
        return obj.user.get_full_name()
    get_full_name.short_description = 'Full Name'


admin.site.register(User, UserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)