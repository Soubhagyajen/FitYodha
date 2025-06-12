from django.urls import path
from .views import home , register, dashboard ,generate_workout, log_workout, leaderboard, blog_list,create_blog, edit_blog, blog_detail, delete_blog, user_profile, toggle_like
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from . import views


urlpatterns = [
    path('', home, name='home'),
     path('login/', LoginView.as_view(template_name='login.html'), name='login'),
     path('logout/', LogoutView.as_view(next_page='home'), name='logout'), 
    path('register/', register, name='register'),
    path('dashboard/', dashboard, name='dashboard'),
    path('generate-workout/', generate_workout, name='generate_workout'),
    path('log-workout/', log_workout, name='log_workout'),
    path('yodha-sabha/', leaderboard, name='leaderboard'),
    path('katha-path/', blog_list, name='blog_list'),
    # path('upload-image/', upload_image_to_supabase, name='upload_image'),
    path('katha/create/', create_blog, name='create_blog'),
    path('katha/edit/<int:pk>/', edit_blog, name='edit_blog'),
    path('katha/<int:pk>/', blog_detail, name='blog_detail'),
    # path('katha/edit/<int:pk>/', edit_blog, name='edit_blog'),
    path('katha/delete/<int:pk>/', delete_blog, name='delete_blog'),
    path('profile/<str:username>/', user_profile, name='user_profile'),
    # path('upload-image/', upload_profile_image, name='upload_profile_image'),
    path('katha/<int:pk>/like/', views.toggle_like, name='toggle_like'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('comment/edit/<int:pk>/', views.edit_comment, name='edit_comment'),

    path('streak-leaderboard/', views.streak_leaderboard, name='streak_leaderboard'),
    path('export-plan/<int:pk>/', views.export_plan_pdf, name='export_plan_pdf'),
    path('generate-diet/', views.generate_diet, name='generate_diet'),
    path('export-diet/<int:pk>/', views.export_diet_pdf, name='export_diet_pdf'),












    # path("", TemplateView.as_view(template_name="home.html"), name="home"),
    # Add more URL patterns as needed
]
