from django.contrib import admin

# Register your models here.
# your_app/admin.py

from django.contrib import admin
from .models import WorkoutLog

@admin.register(WorkoutLog)
class WorkoutLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'workout_type', 'duration', 'intensity', 'date')
    list_filter = ('intensity', 'date')
    search_fields = ('user__username', 'workout_type')



from .models import BlogPost
from django.utils.html import format_html
from django.utils.html import mark_safe

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'image_preview', 'created_at')

    def image_preview(self, obj):
        return mark_safe(f'<img src="{obj.image_url}" width="100" />')


# from .models import Profile
# @admin.register(Profile)
# class ProfileAdmin(admin.ModelAdmin):
#     list_display = ('user', 'image_url')
