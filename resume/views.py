from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import UserUpdateForm, ProfileUpdateForm, UserRegisterForm, EducationForm, WorkExperienceForm, SkillForm
from .models import Profile, Education, WorkExperience, Skill
from django.views.decorators.csrf import csrf_exempt

def index(request):
    context = {}
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        context['profile'] = profile
    return render(request, 'index.html', context)

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('index')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'profile.html', context)


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')  # Redirect to the index page
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')


def signup(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('index')
    else:
        form = UserRegisterForm()
        for field in form.fields.values():
            field.widget.attrs['placeholder'] = field.label
    return render(request, 'signup.html', {'form': form})


@login_required
def education(request):
    if request.method == 'POST':
        schools = request.POST.getlist('school[]')
        degrees = request.POST.getlist('degree[]')
        start_dates = request.POST.getlist('start_date[]')
        end_dates = request.POST.getlist('end_date[]')

        for school, degree, start_date, end_date in zip(schools, degrees, start_dates, end_dates):
            Education.objects.create(
                user=request.user,
                school=school,
                degree=degree,
                start_date=start_date,
                end_date=end_date
            )

        return redirect('education')  # Redirect to the same page to display the updated list

    # Fetch all saved education entries
    education_entries = Education.objects.filter(user=request.user)

    context = {
        'education_entries': education_entries
    }

    return render(request, 'education.html', context)


def education_view(request):
    if request.method == 'POST':
        form = EducationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('education')  # Redirect to the same page to display the updated list
    else:
        form = EducationForm()

    # Fetch all saved education entries
    education_entries = Education.objects.filter(user=request.user)

    context = {
        'form': form,
        'education_entries': education_entries
    }

    return render(request, 'education.html', context)


@login_required
def edit_education(request, education_id):
    education = get_object_or_404(Education, id=education_id, user=request.user)
    if request.method == 'POST':
        form = EducationForm(request.POST, instance=education)
        if form.is_valid():
            form.save()
            return redirect('education')
    else:
        form = EducationForm(instance=education)

    context = {
        'form': form,
        'education_entries': Education.objects.filter(user=request.user)
    }

    return render(request, 'education.html', context)

@login_required
def delete_education(request, education_id):
    education = get_object_or_404(Education, id=education_id, user=request.user)
    if request.method == 'POST':
        education.delete()
        return redirect('education')

    context = {
        'education': education
    }

    return render(request, 'confirm_delete.html', context)


def resume_view(request):
    user = request.user
    profile = user.profile
    education_entries = Education.objects.filter(user=user)
    work_experience_entries = WorkExperience.objects.filter(user=user)
    skills = Skill.objects.filter(user=user)
    
    context = {
        'user': user,
        'profile': profile,
        'education_entries': education_entries,
        'work_experience_entries': work_experience_entries,
        'skills': skills,
    }
    
    return render(request, 'resume.html', context)


@login_required
def work_experience(request):
    if request.method == 'POST':
        form = WorkExperienceForm(request.POST)
        if form.is_valid():
            work_experience = form.save(commit=False)
            work_experience.user = request.user
            work_experience.save()
            return redirect('work_experience')
    else:
        form = WorkExperienceForm()
    
    work_experience_entries = WorkExperience.objects.filter(user=request.user)
    return render(request, 'work_experience.html', {
        'form': form,
        'work_experience_entries': work_experience_entries
    })

@csrf_exempt
def save_work_experience(request):
    if request.method == 'POST':
        company = request.POST.getlist('company[]')
        job_title = request.POST.getlist('job_title[]')
        start_date = request.POST.getlist('start_date[]')
        end_date = request.POST.getlist('end_date[]')
        responsibilities = request.POST.getlist('responsibilities[]')
        achievements = request.POST.getlist('achievements[]')
        skills_used = request.POST.getlist('skills_used[]')

        for i in range(len(company)):
            WorkExperience.objects.create(
                user=request.user,
                company=company[i],
                job_title=job_title[i],
                start_date=start_date[i],
                end_date=end_date[i],
                responsibilities=responsibilities[i],
                achievements=achievements[i],
                skills_used=skills_used[i]
            )

        return redirect('work_experience')  # Redirect to the work experience page or any other page

    return JsonResponse({'error': 'Invalid request'}, status=400)

def edit_work_experience(request, id):
    experience = get_object_or_404(WorkExperience, id=id)
    if request.method == 'POST':
        form = WorkExperienceForm(request.POST, instance=experience)
        if form.is_valid():
            form.save()
            return redirect('work_experience')
    else:
        form = WorkExperienceForm(instance=experience)
    return render(request, 'edit_work_experience.html', {'form': form})

def delete_work_experience(request, id):
    experience = get_object_or_404(WorkExperience, id=id)
    if request.method == 'POST':
        experience.delete()
        return redirect('work_experience')
    return render(request, 'work_confirm_delete.html', {'experience': experience})


@login_required
def save_skill(request):
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.user = request.user
            skill.save()
            return redirect('skills')
    else:
        form = SkillForm()
    return render(request, 'skill.html', {'form': form})

@login_required
def edit_skill(request, skill_id):
    skill = get_object_or_404(Skill, id=skill_id, user=request.user)
    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            return redirect('skills')
    else:
        form = SkillForm(instance=skill)
    return render(request, 'edit_skill.html', {'form': form})

@login_required
def delete_skill(request, skill_id):
    skill = get_object_or_404(Skill, id=skill_id, user=request.user)
    if request.method == 'POST':
        skill.delete()
        return redirect('skills')
    return render(request, 'skill_confirm_delete.html', {'object': skill})

@login_required
def skills(request):
    skill_entries = Skill.objects.filter(user=request.user)
    return render(request, 'skill.html', {'skill_entries': skill_entries})