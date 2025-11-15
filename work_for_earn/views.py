from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Work

# ----------------------
# Add Work
# ----------------------
def add_work_view(request):
    if 'username' not in request.session:
        messages.error(request, "You must log in to add work.")
        return redirect('login')

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        address = request.POST.get('address')
        mobile_number = request.POST.get('mobile_number')
        payment = request.POST.get('payment')
        end_time = request.POST.get('end_time')
        category = request.POST.get('category', 'Physical')
        image = request.FILES.get('image')

        if not title or not description or not mobile_number or not payment:
            messages.error(request, "Please fill all required fields.")
            return redirect('add_work')

        user = User.objects.get(username=request.session['username'])
        work = Work.objects.create(
            title=title,
            description=description,
            address=address,
            mobile_number=mobile_number,
            payment=payment,
            category=category,
            end_time=end_time if end_time else None,
            posted_by=user,
            image=image
        )

        if category == 'Online':
            work.payment_status = 'Paid'  # Admin confirms
            work.save()

        messages.success(request, "Work post added successfully!")
        return redirect('home')

    return render(request, 'add_work.html')


# ----------------------
# Home View
# ----------------------
def home_view(request):
    if 'username' not in request.session:
        return redirect('login')

    username = request.session['username']
    works = Work.objects.filter(status__in=['Pending','Accepted']).order_by('-created_at')
    return render(request, 'home.html', {'username': username, 'posts': works})


# ----------------------
# Accept Work
# ----------------------
def accept_work(request, work_id):
    if 'username' not in request.session:
        messages.error(request, "Login required to accept work.")
        return redirect('login')

    accepter = User.objects.get(username=request.session['username'])
    work = get_object_or_404(Work, id=work_id)

    if work.status == 'Pending' and work.posted_by != accepter:
        work.accepted_by = accepter
        work.status = 'Accepted'
        work.save()
        messages.success(request, "You have accepted the work!")
    else:
        messages.error(request, "Cannot accept this work.")

    return redirect('home')


# ----------------------
# Complete Work
# ----------------------
def complete_work(request, work_id):
    if 'username' not in request.session:
        messages.error(request, "Login required to complete work.")
        return redirect('login')

    user = User.objects.get(username=request.session['username'])
    work = get_object_or_404(Work, id=work_id)

    if work.accepted_by == user and work.status == 'Accepted':
        work.status = 'Completed'
        if work.category == 'Online':
            work.payment_status = 'Paid'  # Admin confirms
        work.save()
        messages.success(request, "Work marked as completed!")
    else:
        messages.error(request, "Cannot complete this work.")

    return redirect('home')


# ----------------------
# Profile View
# ----------------------
def profile_view(request):
    if 'username' not in request.session:
        return redirect('login')

    user = User.objects.get(username=request.session['username'])
    works_posted = Work.objects.filter(posted_by=user).order_by('-created_at')
    works_accepted = Work.objects.filter(accepted_by=user).order_by('-created_at')

    return render(request, 'profile.html', {
        'username': user.username,
        'works_posted': works_posted,
        'works_accepted': works_accepted
    })
