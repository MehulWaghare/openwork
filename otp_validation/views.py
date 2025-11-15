from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from work_for_earn.models import Work
from .models import WorkOTP
import random

def send_otp_view(request, work_id):
    """
    Sends an OTP to the user who posted the work.
    """
    work = get_object_or_404(Work, id=work_id)
    user = work.posted_by  # Only the poster receives the OTP

    # Generate a 6-digit OTP
    otp_code = str(random.randint(100000, 999999))

    # Save or update OTP record in database
    WorkOTP.objects.update_or_create(work=work, defaults={'otp': otp_code})

    # Send OTP via email
    try:
        send_mail(
            subject="Work Completion OTP",
            message=f"Your OTP for work completion is {otp_code}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )
        messages.success(request, f"OTP sent successfully to {user.email}")
    except Exception as e:
        messages.error(request, f"Failed to send OTP email: {e}")

    # Redirect to OTP validation page
    return redirect('validate_otp', work_id=work.id)


def validate_otp_view(request, work_id):
    """
    Validates the OTP entered by the poster to mark the work as completed.
    """
    work = get_object_or_404(Work, id=work_id)
    otp_record = WorkOTP.objects.filter(work=work).first()

    if request.method == "POST":
        entered_otp = request.POST.get("otp")

        if otp_record and otp_record.otp == entered_otp:
            # Mark work as completed
            work.status = "Completed"
            work.save()
            otp_record.delete()  # Remove OTP after successful validation
            messages.success(request, f"Work '{work.title}' marked as completed!")
            return redirect('profile')
        else:
            messages.error(request, "Invalid OTP. Please try again.")

    return render(request, "validate_otp.html", {"work": work})
