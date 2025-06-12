from django.shortcuts import render 
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import WorkoutLogForm
from .models import WorkoutLog
from django.db.models import Count
from django.contrib.auth.models import User
from .models import BlogPost, Comment
# from .forms import SupabaseImageUploadForm
import requests
import uuid
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from .forms import BlogPostForm
from .models import BlogPost, Profile, Comment, WorkoutPlan, DietPlan
import requests, uuid
from django.conf import settings
# from .forms import ProfileImageUploadForm
from django.http import HttpResponseForbidden

# Create your views here.

def home(request):
    return render(request, 'main/home.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your Yodha account has been created. You can now log in.")
            return redirect('login')
    else:
        form = UserCreationForm()
    
    return render(request, 'register.html', {'form': form})



from .models import WorkoutLog

# @login_required
# def dashboard(request):
#     recent_logs = WorkoutLog.objects.filter(user=request.user).order_by('-date')[:5]
#     user_plans = WorkoutPlan.objects.filter(user=request.user).order_by('-created_at')[:1]

#     # Optional: Karma Score = 10 points per workout
#     karma_score = WorkoutLog.objects.filter(user=request.user).count() * 10
    
#     user_diets = DietPlan.objects.filter(user=request.user).order_by('-created_at')[:1]
#     return render(request, 'main/dashboard.html', {
#         'logs': recent_logs,
#         'plans': user_plans,
#         'diets': user_diets
#     })

#     return render(request, 'main/dashboard.html', {
#         'recent_logs': recent_logs,
#         'karma_score': karma_score,
#         'plans': user_plans
#     })

from django.utils import timezone
from datetime import timedelta

from datetime import date, timedelta

@login_required
def dashboard(request):
    user = request.user
    today = date.today()

    recent_logs = WorkoutLog.objects.filter(user=user).order_by('-date')[:5]
    user_plans = WorkoutPlan.objects.filter(user=user).order_by('-created_at')[:1]
    user_diets = DietPlan.objects.filter(user=user).order_by('-created_at')[:1]
    karma_score = WorkoutLog.objects.filter(user=user).count() * 10

    # Streak warning logic
    streak_warning = False
    if user.profile.last_workout_date == today - timedelta(days=1) and not user.profile.freeze_used:
        streak_warning = True

    return render(request, 'main/dashboard.html', {
        'recent_logs': recent_logs,
        'plans': user_plans,
        'diets': user_diets,
        'karma_score': karma_score,
        'streak_warning': streak_warning,
    })



import random
from .models import WorkoutPlan

WORKOUT_LIBRARY = {
    "Build Muscle": [
        "Pushups - 3x15",
        "Dumbbell Rows - 3x12",
        "Squats - 3x20",
        "Plank - 1 min",
        "Lunges - 3x12 each leg"
    ],
    "Lose Fat": [
        "Jumping Jacks - 3x50",
        "Burpees - 3x15",
        "High Knees - 3x40",
        "Mountain Climbers - 3x30",
        "Skipping - 3 mins"
    ],
    "Gain Strength": [
        "Pull-ups - 3x5",
        "Deadlifts - 3x8",
        "Overhead Press - 3x10",
        "Front Squats - 3x10"
    ]
}

DIET_LIBRARY = {
    "Build Muscle": [
        "Day 1: Oats + Eggs, Chicken + Rice, Nuts",
        "Day 2: Smoothie, Paneer Wrap, Milk",
        "Day 3: Dosa + Peanut Butter, Grilled Fish, Banana",
        "Day 4: Boiled Eggs, Dal + Roti, Curd",
        "Day 5: Protein Shake, Chicken Curry, Apple",
        "Day 6: Idli + Eggs, Brown Rice + Dal, Greek Yogurt",
        "Day 7: Cheat day 🍕 (balance with fruits)"
    ],
    "Lose Fat": [
        "Day 1: Green Tea, Upma, Veg Curry",
        "Day 2: Fruit Bowl, Sprouts, Lemon Rice",
        "Day 3: Smoothie, Roti + Sabzi, Coconut Water",
        "Day 4: Poha, Salad, Buttermilk",
        "Day 5: Dhokla, Brown Rice, Boiled Veggies",
        "Day 6: Soup, Khichdi, Green Tea",
        "Day 7: Detox Day 🥒"
    ]
}

def generate_diet_with_huggingface(goal, level):
    url = "https://api-inference.huggingface.co/models/MBZUAI/LaMini-Flan-T5-783M"
    headers = {"Authorization": f"Bearer {settings.HUGGINGFACE_API_KEY}"}

    prompt = f"Generate a 7-day vegetarian diet plan for a {level.lower()} person whose goal is to {goal.lower()}."

    try:
        response = requests.post(url, headers=headers, json={"inputs": prompt}, timeout=60)
        if response.status_code == 200:
            result = response.json()
            return result[0]['generated_text'] if isinstance(result, list) else result.get('generated_text', '')
        return f"❌ Error {response.status_code}: {response.text}"
    except Exception as e:
        return f"💥 Exception: {str(e)}"

@login_required
def generate_diet(request):
    if request.method == 'POST':
        goal = request.POST.get('goal')
        level = request.POST.get('level')

        diet_list = DIET_LIBRARY.get(goal, [])
        plan_text = f"{level} {goal} Diet Plan\n" + "-"*30 + "\n" + "\n".join(diet_list)

        DietPlan.objects.create(
            user=request.user,
            goal=goal,
            level=level,
            plan_text=plan_text
        )
        return redirect('dashboard')

    return render(request, 'main/generate_diet.html', {'goals': DIET_LIBRARY.keys()})


from xhtml2pdf import pisa
from django.template.loader import render_to_string
from django.http import HttpResponse

@login_required
def export_diet_pdf(request, pk):
    diet = get_object_or_404(DietPlan, pk=pk, user=request.user)
    html = render_to_string('main/pdf_diet_template.html', {'diet': diet})

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=DietPlan_{diet.goal}_{diet.level}.pdf'

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Failed to generate PDF', status=500)
    
    return response


import requests
from django.conf import settings

# def generate_plan_with_huggingface(prompt):
#     url = "https://huggingface.co/Qwen/Qwen3-Reranker-0.6B"
#     headers = {"Authorization": f"Bearer {settings.HUGGINGFACE_API_KEY}"}

#     try:
#         response = requests.post(url, headers=headers, json={"inputs": prompt}, timeout=60)
#         if response.status_code == 200:
#             result = response.json()
#             return result[0]['generated_text'] if isinstance(result, list) else result.get('generated_text', '')
#         elif response.status_code == 503:
#             return "⏳ Model is warming up. Please try again shortly."
#         else:
#             return f"❌ Error {response.status_code}: {response.text}"
#     except Exception as e:
#         return f"💥 Exception: {str(e)}"

@login_required
def generate_workout(request):
    if request.method == 'POST':
        goal = request.POST.get('goal')
        level = request.POST.get('level')

        # Fallback only using local list
        exercise_list = WORKOUT_LIBRARY.get(goal, [])
        exercises = random.sample(exercise_list, k=min(len(exercise_list), 4))

        plan_text = f"{level} {goal} Plan\n" + "-"*30 + "\n" + "\n".join(exercises)

        # Save to DB
        WorkoutPlan.objects.create(
            user=request.user,
            goal=goal,
            level=level,
            plan_text=plan_text
        )

        return redirect('dashboard')

    return render(request, 'main/generate_workout.html', {'goals': WORKOUT_LIBRARY.keys()})










from xhtml2pdf import pisa
from django.http import HttpResponse
from django.template.loader import render_to_string

@login_required
def export_plan_pdf(request, pk):
    plan = get_object_or_404(WorkoutPlan, pk=pk, user=request.user)
    html = render_to_string('main/pdf_template.html', {'plan': plan})
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="WorkoutPlan_{plan.goal}_{plan.level}.pdf"'

    pisa.CreatePDF(html, dest=response)
    return response


@login_required
def log_workout(request):
    message = None
    if request.method == 'POST':
        form = WorkoutLogForm(request.POST)
        if form.is_valid():
            workout = form.save(commit=False)
            workout.user = request.user
            workout.save()
            message = "Workout logged successfully!"
            form = WorkoutLogForm()
            try:
                update_streak(request.user)
            except Profile.DoesNotExist:
                Profile.objects.create(user=request.user)
                update_streak(request.user)

    else:
        form = WorkoutLogForm()

    return render(request, 'main/log_workout.html', {'form': form, 'message': message})



from datetime import date, timedelta

def update_streak(user):
    profile = user.profile
    today = date.today()

    if profile.last_workout_date == today:
        return  # Already counted today

    if profile.last_workout_date == today - timedelta(days=1):
        # Normal streak increase
        profile.streak += 1
        profile.freeze_used = False  # Reset freeze for next miss
    elif profile.last_workout_date == today - timedelta(days=2) and not profile.freeze_used:
        # Missed 1 day, use freeze
        profile.freeze_used = True
        # Don't increase, but don't reset
    else:
        # Missed >1 day or already used freeze
        profile.streak = 1
        profile.freeze_used = False

    profile.last_workout_date = today
    profile.save()



from django.contrib.auth.models import User
from .models import Profile

@login_required
def streak_leaderboard(request):
    top_profiles = Profile.objects.select_related('user').order_by('-streak')[:10]
    return render(request, 'main/streak_leaderboard.html', {'top_profiles': top_profiles})


@login_required
def leaderboard(request):
    # Annotate users with workout count
    user_stats = User.objects.annotate(
        total_workouts=Count('workoutlog')
    ).filter(total_workouts__gt=0).order_by('-total_workouts')[:10]  # Top 10

    # If you want, you can add derived fields here, e.g. multiply total_workouts by a factor
    # Example: add 'score' which is total_workouts * 10
    for user in user_stats:
        user.score = user.total_workouts * 10  # multiply here in Python, no need for template filter

    return render(request, 'main/leaderboard.html', {'user_stats': user_stats})




def blog_list(request):
    posts = BlogPost.objects.order_by('-created_at')
    return render(request, 'main/blog_list.html', {'posts': posts})



# @login_required
# def upload_image_to_supabase(request):
#     image_url = None

#     if request.method == 'POST':
#         form = SupabaseImageUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             file = form.cleaned_data['image']
#             file_ext = file.name.split('.')[-1]
#             unique_filename = f"{uuid.uuid4()}.{file_ext}"

#             upload_url = f"{settings.SUPABASE_URL}/storage/v1/object/{settings.SUPABASE_BUCKET}/{unique_filename}"
#             headers = {
#                 'apikey': settings.SUPABASE_API_KEY,
#                 'Authorization': f'Bearer {settings.SUPABASE_API_KEY}',
#                 'Content-Type': 'application/octet-stream'
#             }

#             response = requests.put(upload_url, headers=headers, data=file.read())

#             if response.status_code in [200, 201]:
#                 image_url = f"{settings.SUPABASE_URL}/storage/v1/object/public/{settings.SUPABASE_BUCKET}/{unique_filename}"
#             else:
#                 print("Upload error:", response.status_code, response.text)

#     else:
#         form = SupabaseImageUploadForm()

#     return render(request, 'main/upload_image.html', {'form': form, 'image_url': image_url})



@login_required
def create_blog(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            return redirect('blog_list')
    else:
        form = BlogPostForm()
    return render(request, 'main/create_blog.html', {'form': form})

@login_required
def edit_blog(request, pk):
    blog = get_object_or_404(BlogPost, pk=pk, author=request.user)
    if blog.author != request.user:
        return HttpResponseForbidden("You are not allowed to edit this blog.")
    if request.method == 'POST':
        form = BlogPostForm(request.POST, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('blog_list')
    else:
        form = BlogPostForm(instance=blog)
    return render(request, 'main/edit_blog.html', {'form': form, 'blog': blog})



from django.contrib.auth.models import User

from .forms import CommentForm

@login_required
def blog_detail(request, pk):
    blog = get_object_or_404(BlogPost, pk=pk)
    comments = blog.comments.order_by('-created_at')
    blog.views += 1
    blog.save()


    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog = blog
            comment.author = request.user
            comment.save()
            return redirect('blog_detail', pk=pk)
    else:
        form = CommentForm()

    return render(request, 'main/blog_detail.html', {
        'blog': blog,
        'form': form,
        'comments': comments,
    })


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)

    if comment.author != request.user:
        return HttpResponseForbidden("You are not allowed to delete this comment.")

    blog_pk = comment.blog.pk
    comment.delete()
    return redirect('blog_detail', pk=blog_pk)



from .forms import CommentForm

@login_required
def edit_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    if comment.author != request.user:
        return HttpResponseForbidden("You cannot edit this comment.")

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('blog_detail', pk=comment.blog.pk)
    else:
        form = CommentForm(instance=comment)

    return render(request, 'main/edit_comment.html', {
        'form': form,
        'comment': comment
    })


@login_required
def toggle_like(request, pk):
    blog = get_object_or_404(BlogPost, pk=pk)

    if request.method == 'POST':
        if request.user in blog.likes.all():
            blog.likes.remove(request.user)
        else:
            blog.likes.add(request.user)

    # ✅ Redirect to the correct blog detail page
    return redirect('blog_detail', pk=pk)



@login_required
def delete_blog(request, pk):
    blog = get_object_or_404(BlogPost, pk=pk, author=request.user)
    if blog.author != request.user:
        return HttpResponseForbidden("You are not allowed to delete this blog.")
    if request.method == 'POST':
        blog.delete()
        return redirect('blog_list')
    return render(request, 'main/confirm_delete.html', {'blog': blog})

@login_required
def user_profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    posts = BlogPost.objects.filter(author=profile_user).order_by('-created_at')
    return render(request, 'main/user_profile.html', {'profile_user': profile_user, 'posts': posts})





import uuid, requests
from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# from .forms import ProfileImageUploadForm

# @login_required
# def upload_profile_image(request):
#     image_url = None
#     error = None

#     if request.method == 'POST':
#         form = ProfileImageUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             image = form.cleaned_data['image']
#             ext = image.name.split('.')[-1]
#             filename = f"profile_{uuid.uuid4()}.{ext}"

#             upload_url = f"{settings.SUPABASE_URL}/storage/v1/object/{settings.SUPABASE_BUCKET}/{filename}"
#             headers = {
#                 "Authorization": f"Bearer {settings.SUPABASE_API_KEY}",
#                 "apikey": settings.SUPABASE_API_KEY,
#                 "Content-Type": "application/octet-stream"
#             }

#             response = requests.put(upload_url, headers=headers, data=image.read())

#             if response.status_code in [200, 201]:
#                 image_url = f"{settings.SUPABASE_URL}/storage/v1/object/public/{settings.SUPABASE_BUCKET}/{filename}"
#                 request.user.profile.image_url = image_url
#                 request.user.profile.save()
#             else:
#                 error = f"Upload failed: {response.status_code} - {response.text}"

#     else:
#         form = ProfileImageUploadForm()

#     return render(request, 'upload_profile_image.html', {
#         'form': form,
#         'image_url': image_url,
#         'error': error
#     })



