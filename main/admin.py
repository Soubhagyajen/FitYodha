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

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'image_preview')
    readonly_fields = ['image_preview']
    search_fields = ('title', 'author__username')

    def image_preview(self, obj):
        if obj.image_url:
            return format_html('<img src="{}" style="max-height: 100px; border-radius: 8px;" />', obj.image_url)
        return "No Image"
    
    image_preview.short_description = 'Preview'

# from .models import Profile
# @admin.register(Profile)
# class ProfileAdmin(admin.ModelAdmin):
#     list_display = ('user', 'image_url')
