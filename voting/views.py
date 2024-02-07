import base64
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from users.forms import UserUpdateForm
from .models import VotingSession, VoteUser, Candidate
from users.models import Profile
from .forms import ContactForm, PositionForm, CandidateForm, UserRegisterForm
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User

from django.shortcuts import render
from .models import VoteUser

from .utils import calculate_percentage  # Import the function to calculate percentage


# Dashboard Overview
@login_required
def admin_dashboard(request):
    return render(request, 'adminpage.html')

def index(request):
    return render(request,'index.html', {})

@login_required
def dashboard(request):
    return render(request, 'dashboard.html', {'dashboard': VotingSession.objects.filter(active=True)})

@login_required
def results_dashboard(request):
    return render(request, 'results.html', {
        'active_sessions': VotingSession.objects.filter(active=True),
        'inactive_sessions': VotingSession.objects.filter(active=False)
    })

@login_required
def votedash(request, pk):
    return render(request, 'votedash.html', {'voting': get_object_or_404(VotingSession, pk=pk)})


def results_detail(request, pk):
    voting_session = get_object_or_404(VotingSession, pk=pk)
    labels, data = generate_statistics_and_context(voting_session)
    labels_chart, data_chart = str(labels).replace("'", '"'), str(data).replace("'", '"')

    return render(request, 'results_detail.html', {
        'voting_session': voting_session,
        'labels': labels,
        'data': data,
        'labels_chart': labels_chart,
        'data_chart': data_chart
    })


def about_page(request):
    return render(request, 'about.html', {})


def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            sender_name = form.cleaned_data['name']
            sender_email = form.cleaned_data['email']
            message = "{0} has sent you a new message:\n\n{1}".format(sender_name, form.cleaned_data['message'])
            send_mail('Support Request', message, sender_email, [settings.EMAIL_HOST_USER])

            messages.success(request, f'The message has been sent! We will contact you shortly.')

            return redirect('contact')
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})

@login_required     
def vote(request, candidate_id, voting_session_id):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect unauthenticated users to the login page

    user = request.user
    user_profile = user.profile
    can_vote = face_recog(settings.MEDIA_ROOT + '/webcamimages/' + user.username + '.jpg', user_profile.image.path)

    if user_profile.image.name == settings.GLOBAL_SETTINGS.get('default_image'):
        return redirect('profile')  # Redirect users with the default image to their profile

    if not can_vote:
        messages.warning(request, "The vote is not valid")
    else:
        candidate = Candidate.objects.get(pk=candidate_id)
        voting_session = VotingSession.objects.get(pk=voting_session_id)
        if not user_has_voted(voting_session, user):
            user_vote = VoteUser(candidate=candidate, voting_session=voting_session, user=user)
            user_vote.save()
            messages.success(request, 'Your vote has been registered successfully!')
        else:
            messages.warning(request, 'You have already voted in this election!')

    return redirect(reverse('votedash', kwargs={'pk': voting_session_id}))


def user_has_voted(voting_session, user):
    return VoteUser.objects.filter(voting_session=voting_session, user=user).exists()

def generate_statistics_and_context(voting_session):
    labels, data = [], []
    votes = VoteUser.objects.all().filter(voting_session=voting_session)
    for candidate in voting_session.candidates.all():
        labels.append(candidate.name)
        data.append(len(list(filter(lambda c: c.candidate_id == candidate.pk, votes))))

    return labels, data

def face_recog(webcam_photo, user_photo):
    import face_recognition

    try:
        picture_of_me = face_recognition.load_image_file(user_photo)
        my_face_encoding = face_recognition.face_encodings(picture_of_me)[0]

        unknown_picture = face_recognition.load_image_file(webcam_photo)
        unknown_face_encoding = face_recognition.face_encodings(unknown_picture)[0]

        results = face_recognition.compare_faces([my_face_encoding], unknown_face_encoding)
        return results[0]

    except Exception as e:
        return False

@csrf_exempt
def save_image(request):
    imgstr = request.POST['mydata']
    voting_session_id = request.POST['voting_session']
    user = request.user.username

    if request.POST:
        f = open(settings.MEDIA_ROOT + '/webcamimages/' + user + '.jpg', 'wb')
        f.write(base64.b64decode(imgstr))
        f.close()

    messages.success(request, f'A picture of your face has been saved in the system!')

    return redirect(reverse('votedash', kwargs={'pk': voting_session_id}))

@login_required
def adminpage(request):
    candidates = Candidate.objects.all()
    vote = VoteUser.objects.all()
    candidate_count = Candidate.objects.all().count()
    voter_count = Profile.objects.all().count()
    position_count = VotingSession.objects.all().count()
    voted_count = VoteUser.objects.all().count()
    context = {
        'candidates': candidates,
        'vote': vote,
        'candidate_count' : candidate_count,
        'voter_count' : voter_count,
        'position_count' : position_count,
        'voted_count' : voted_count,
    }
    return render(request,'adminpage.html', context)

@login_required
def logout(request):
    return render(request,'index.html')

# Manage candidates
def View_candidate(request):
    candidates = Candidate.objects.all()
    return render(request, 'View_candidate.html', {'candidates': candidates})

def add_candidate(request):
    if request.method == "POST":
        form = CandidateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('View_candidate')
        else:
            print(form.errors)  # Check the console for form validation errors
    else:
        form = CandidateForm()

    return render(request, "Add_candidate.html", {'form': form})

def delete_candidate(request, id):
    candidate = Candidate.objects.get(pk=id)
    candidate.delete()
    return redirect(reverse('View_candidate'))

def update_candidate(request, id):
    candidate = Candidate.objects.get(pk=id)

    if request.method == "POST":
        form = CandidateForm(request.POST, request.FILES, instance=candidate)
        if form.is_valid():
            form.save()
            return redirect(reverse('View_candidate'))
    else:
        form = CandidateForm(instance=candidate)
    context = {"form": form, "candidate": candidate}
    return render(request, "updat_candidates.html", context)

# Manage positions
def add_position(request):
    if request.method == "POST":
        form = PositionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('View_position')
        else:
            print(form.errors)  # Check the console for form validation errors
    else:
        form = PositionForm()

    return render(request, "Add_position.html", {'form': form})

def View_position(request):
    positions = VotingSession.objects.all()
    return render(request,'View_position.html', {'positions': positions})

def delete_position(request, id):
    position = VotingSession.objects.get(pk=id)
    position.delete()
    return redirect(reverse('View_position'))

def update_position(request, id):
    position = VotingSession.objects.get(pk=id)

    if request.method == "POST":
        form = PositionForm(request.POST, request.FILES, instance=position)
        if form.is_valid():
            form.save()
            return redirect(reverse('View_position'))
    else:
        form = PositionForm(instance=position)
    context = {"form": form, "position": position}
    return render(request, "update_positions.html", context)

# Manage voters
def add_voter(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('View_voter')
        else:
            print(form.errors)  # Check the console for form validation errors
    else:
        form = UserRegisterForm()

    return render(request, "Add_voter.html", {'form': form})

def View_voter(request):
    voters = User.objects.all()
    return render(request, 'View_voter.html', {'voters': voters})

def delete_voter(request, id):
    voter = User.objects.get(pk=id)
    voter.delete()
    return redirect(reverse('View_voter'))

def update_voter(request, id):
    voter = User.objects.get(pk=id)

    if request.method == "POST":
        form = UserRegisterForm(request.POST, request.FILES, instance=voter)
        if form.is_valid():
            form.save()
            return redirect(reverse('View_voter'))
    else:
        form = UserRegisterForm(instance=voter)
    context = {"form": form, "voter": voter}
    return render(request, "update_voters.html", context)

# Manage results
def Create_report(request):
    return render(request,'Create_report.html', {})

def View_result(request):
    return render(request,'View_result.html', {})


# Print function
def print_page(request):
    return render(request, 'adminpage.html')

def voted_users_list(request):
    voted_users = VoteUser.objects.all()
    return render(request, 'View_votedUsers.html', {'voted_users': voted_users})