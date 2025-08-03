from django.db import models

# Create your models here.


from django.db import models
from django.contrib.auth.models import User

class WorkoutLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    workout_type = models.CharField(max_length=100)
    duration = models.IntegerField(help_text="Duration in minutes")
    intensity = models.CharField(max_length=20, choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')])
    date = models.DateField(auto_now_add=True)
    image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.workout_type} on {self.date}"


# models.py
class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    image_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    views = models.IntegerField(default=0)

    def reading_time(self):
        words = len(self.content.split())
        return max(1, words // 200)  # ~200 words per minute

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image_url = models.URLField(blank=True, null=True)  # Add this back
    streak = models.IntegerField(default=0)
    last_workout_date = models.DateField(null=True, blank=True)
    freeze_used = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s Profile"


class Comment(models.Model):
    blog = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username} on {self.blog.title}"



class WorkoutPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goal = models.CharField(max_length=100)  # e.g. "Build Muscle"
    level = models.CharField(max_length=50, default="Beginner")
    plan_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Plan - {self.goal}"

class DietPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goal = models.CharField(max_length=100)
    level = models.CharField(max_length=50, default="Beginner")
    plan_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Diet Plan - {self.goal}"
