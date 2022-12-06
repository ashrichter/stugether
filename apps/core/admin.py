from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import CreateUserForm, ChangeUserForm


class UserAdmin(BaseUserAdmin):
    add_form = CreateUserForm
    form = ChangeUserForm
    model = User
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('type', 'bio', 'status', 'date_of_birth',
                           'institution', 'field_of_study',
                           'contribution_counter', 'profile_image', 'well_being_visibility')}),
    )


class TopicAdmin(admin.ModelAdmin):
    model = Topic
    list_display = ['id', 'title', 'type', 'description', 'created_at', ]


class InterestAdmin(admin.ModelAdmin):
    model = Interest
    list_display = ['user', 'topic']


class FriendAdmin(admin.ModelAdmin):
    model = Friend
    list_display = ['id', 'sender', 'receiver', 'accepted']


admin.site.register(User, UserAdmin)
admin.site.register(Interest, InterestAdmin)
admin.site.register(Friend, FriendAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Institution)
admin.site.register(Subject)
