from django.http import HttpResponse
# from django.shortcuts import render 

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required

from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib import messages


from django.core.mail import send_mail
from .models import EmailOTP
import random
from django.contrib.auth.models import User

from django.shortcuts import render, get_object_or_404
# from .models import Program, Semester, Note

def send_otp_to_email(email):
    otp = str(random.randint(100000, 999999))

    EmailOTP.objects.update_or_create(
        email=email,
        defaults={'otp': otp}
    )

    send_mail(
        subject="Your OTP Verification Code",
        message=f"Your OTP code is: {otp}",
        from_email="mahipalsinghraomp@gmail.com",
        recipient_list=[email],
    )

def auth_page(request):
    register_form = RegisterForm()
    login_form = AuthenticationForm()
    if request.method == 'POST':
        if 'send_otp' in request.POST:
            email = request.POST.get('email')

# 1. Validate email format
            try:
                validate_email(email)
            except ValidationError:
                messages.error(request, "Invalid email format.")
                return redirect('auth_page')
            
            if not email.lower().endswith("@spsu.ac.in"):
                messages.error(request, "Only spsu.ac.in email addresses are allowed.")
                return redirect('auth_page')
            
            if User.objects.filter(email=email).exists():
                messages.error(request, "An account with this email already exists.")
                return redirect('auth_page')
            request.session['pending_email'] = email


# 2. Try sending email safely — catch all exceptions
            try:
                send_otp_to_email(email)
            except Exception as e:
                messages.error(request, "Email does not exist or cannot receive messages.")
                return redirect('auth_page')

            messages.success(request, "OTP sent successfully!")
            return redirect('verify_otp')

        elif 'login' in request.POST:  
            register_form = RegisterForm()
            login_form = AuthenticationForm(request, data=request.POST)
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                return redirect('home')

        else:
            register_form = RegisterForm()
            login_form = AuthenticationForm()

    return render(request, 'accounts/auth.html', {
        'register_form': register_form,
        'login_form': login_form,
    })

def verify_otp(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        email = request.session.get('pending_email')

        if not email:
            messages.error(request, "Session expired. Try again.")
            return redirect('auth_page')

        record = EmailOTP.objects.filter(email=email).first()

        if record and record.otp == entered_otp:

            # OTP correct → move to step 3
            return redirect('complete_registration')

        else:
            messages.error(request, "Invalid OTP, try again.")

    return render(request, 'accounts/verify_otp.html')

def complete_registration(request):
    email = request.session.get('pending_email')

    if not email:
        return redirect('auth_page')

    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
        else:
            User.objects.create_user(
                username=username,
                email=email,
                password=password1
            )

            # Clear session
            del request.session['pending_email']

            messages.success(request, "Registration complete! You can login now.")
            return redirect('auth_page')

    return render(request, 'accounts/complete_registration.html')

# part2
def pdf_viewer(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    return render(request, "accounts/pdfviewer.html", {
        "pdf_url": note.file.url,
        "note_id": note.id
    })

import requests
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from ProgramPage.models import Note
from .import utils

from .utils import (
    extract_text_from_pdf,
    get_pdf_page_count,
    calculate_target_words,
    generate_adaptive_summary,
    generate_exam_questions,
    generate_topics,
    trim_text_by_words,
    clean_pdf_text,
    is_bad_extraction,
    generate_page_wise_summary,
)
def serve_pdf(request, note_id):
    note = get_object_or_404(Note, id=note_id)

    # Cloudflare PDF URL (private or public)
    cloudflare_url = note.file.url

    r = requests.get(cloudflare_url, stream=True)
    r.raise_for_status()

    response = HttpResponse(
        r.content,
        content_type="application/pdf"
    )

    response["Content-Disposition"] = "inline; filename=note.pdf"
    return response

def pdf_ai_tools(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    tool_type = request.GET.get("type")
    text = None
    if tool_type in ["mcq", "exam", "topics"]:
        text = extract_text_from_pdf(note.file.url)

    if tool_type == "summary":
        result = generate_page_wise_summary(
        note.file.url,
        sentences_per_page=3
        )

    elif tool_type == "exam":
        result = generate_exam_questions(text)
    elif tool_type == "topics":
        result = generate_topics(text)
    else:
        return JsonResponse({"error": "Invalid option selected"}, status=400)

    response = {"result": result}

        # if tool_type == "summary" and actual_pages > used_pages:
        #     response["warning"] = (
        #         "This summary covers only the first part of the document."
        #     )

    return JsonResponse(response)
