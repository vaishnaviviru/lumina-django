from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.timezone import now
from django.contrib import messages
import markdown2

from .forms import RegisterForm
from .models import Profile, Showcase

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            Profile.objects.create(user=user)  # Create linked profile
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def dashboard(request):
    profile = request.user.profile
    showcases = profile.showcases.all()
    return render(request, 'clac/dashboard.html', {
        'profile': profile,
        'showcases': showcases
    })
from django.utils.timezone import now
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def review_queue(request):
    pending = Showcase.objects.filter(approved=False)
    return render(request, 'clac/admin_review.html', {'pending': pending})

@staff_member_required
def approve_showcase(request, id):
    if request.method == 'POST':
        print("✅ approve_showcase view hit")
        coins = int(request.POST.get('coins', 0))
        showcase = get_object_or_404(Showcase, id=id)
        showcase.approved = True
        showcase.coins_award = coins
        showcase.approved_at = now()
        showcase.save()

        profile = showcase.owner
        profile.coins += coins
        profile.update_tier()
        profile.save()  # <-- Without this, the coin change won't persist

        messages.success(request, f'Showcase approved and {coins} coins awarded.')
    return redirect('review_queue')


@staff_member_required
def reject_showcase(request, id):
    if request.method == 'POST':
        reason = request.POST.get('reason', '')
        showcase = get_object_or_404(Showcase, id=id)
        showcase.admin_note = reason
        showcase.save()
        messages.warning(request, f'Showcase rejected with reason: {reason}')
    return redirect('review_queue')
from django.shortcuts import render, get_object_or_404
from .models import Showcase

def showcase_detail(request, id):
    showcase = get_object_or_404(Showcase, id=id)

    # ✅ Convert markdown with extras
    body_html = markdown2.markdown(
        showcase.body_md,
        extras=["fenced-code-blocks", "code-friendly", "highlightjs-lang"]
    )

    return render(request, 'clac/showcase_detail.html', {
        'showcase': showcase,
        'body_html': body_html,
    })
def leaderboard(request):
    profiles = Profile.objects.order_by('-coins', 'joined')[:10]
    return render(request, 'clac/leaderboard.html', {'profiles': profiles})
@login_required
def profile_view(request):
    profile = request.user.profile
    showcases = profile.showcases.all()
    return render(request, 'clac/profile.html', {
        'profile': profile,
        'showcases': showcases,
    })
from .forms import ShowcaseForm

@login_required
def add_showcase(request):
    if request.method == 'POST':
        form = ShowcaseForm(request.POST, request.FILES)
        if form.is_valid():
            showcase = form.save(commit=False)
            showcase.owner = request.user.profile
            showcase.save()
            return redirect('dashboard')
    else:
        form = ShowcaseForm()
    return render(request, 'clac/add_showcase.html', {'form': form})
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            Profile.objects.create(user=user)
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})
@staff_member_required
def reject_showcase(request, id):
    if request.method == 'POST':
        reason = request.POST.get('reason', '')
        showcase = get_object_or_404(Showcase, id=id)
        showcase.admin_note = reason
        showcase.save()
        messages.warning(request, f'Showcase rejected with reason: {reason}')
    return redirect('review_queue')






