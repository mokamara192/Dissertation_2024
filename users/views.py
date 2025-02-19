from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from voting.models import VotingSession, Candidate, VoteUser
from .models import Profile
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.admin.views.decorators import staff_member_required


# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your account has been created! You are now able to log in!')
            return redirect('profile')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

# 
@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        if settings.GLOBAL_SETTINGS.get('default_image') in request.user.profile.image.path:
            messages.warning(request,
                             f'In order to be able to vote, please update your profile and provide a picture of your face!')
    return render(request, 'profile.html', {'u_form': u_form, 'p_form': p_form})



    # EC_admin view functins
# def manage_voters(request):
#     voters = Profile.objects.all()
#     return render(request, 'manage_voters.html', {'voters': voters})

# def manage_voting_sessions(request):
#     sessions = VotingSession.objects.all()
#     return render(request, 'manage_voting_sessions.html', {'sessions': sessions})

# def manage_candidate(request):
#     candidate = Candidate.objects.all()
#     return render(request, 'manage_candidate.html', {'candidate': candidate})

# def manage_voteuser(request):
#     voteuser = VoteUser.objects.all()
#     return render(request, 'manage_voteuser.html', {'voteuser': voteuser})
