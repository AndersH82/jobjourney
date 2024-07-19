from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('profile/', views.profile, name='profile'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('education/', views.education, name='education'),
    path('save_education/', views.education, name='save_education'),
    path('education/edit/<int:education_id>/', views.edit_education, name='edit_education'),
    path('education/delete/<int:education_id>/', views.delete_education, name='delete_education'),
    path('resume/', views.resume_view, name='resume'),
    path('work_experience/', views.work_experience, name='work_experience'),
    path('save_work_experience/', views.save_work_experience, name='save_work_experience'),
    path('edit_work_experience/<int:id>/', views.edit_work_experience, name='edit_work_experience'),
    path('delete_work_experience/<int:id>/', views.delete_work_experience, name='delete_work_experience'),
    path('skills/', views.skills, name='skills'),
    path('skills/save/', views.save_skill, name='save_skill'),
    path('skills/edit/<int:skill_id>/', views.edit_skill, name='edit_skill'),
    path('skills/delete/<int:skill_id>/', views.delete_skill, name='delete_skill'),
]