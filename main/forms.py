from django import forms
from .models import WorkoutLog
from django import forms
from .models import BlogPost, Profile, Comment


class WorkoutLogForm(forms.ModelForm):
    class Meta:
        model = WorkoutLog
        fields = ['workout_type', 'duration', 'intensity']
        widgets = {
            'workout_type': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 rounded-lg bg-steel-800 text-white border border-steel-700 focus:outline-none focus:ring-2 focus:ring-saffron-500'
            }),
            'duration': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 rounded-lg bg-steel-800 text-white border border-steel-700 focus:outline-none focus:ring-2 focus:ring-saffron-500'
            }),
            'intensity': forms.Select(attrs={
                'class': 'w-full px-4 py-2 rounded-lg bg-steel-800 text-white border border-steel-700 focus:outline-none focus:ring-2 focus:ring-saffron-500'
            })
        }



# class SupabaseImageUploadForm(forms.Form):
#     image = forms.ImageField(required=True)





class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 rounded bg-steel-900 text-white border border-steel-600 focus:outline-none focus:ring-2 focus:ring-saffron-500'
            }),
            'content': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 rounded bg-steel-900 text-white border border-steel-600 focus:outline-none focus:ring-2 focus:ring-saffron-500',
                'rows': 8
            }),
        }


# class ProfileImageUploadForm(forms.Form):
#     image = forms.ImageField()



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 2, 'class': 'w-full rounded p-2 bg-steel-800 text-white border border-steel-700'})
        }
