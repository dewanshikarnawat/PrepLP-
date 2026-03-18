from ProgramPage.models import Note, Semester, Subject, PYQ, NoteRequest
from django.shortcuts import get_object_or_404, render

from django.http import HttpResponse
# from django.shortcuts import render 

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib import messages

import random
from django.contrib.auth.models import User
from ProgramPage.models import Program, Semester, Note

@login_required
def home(request):
    programs = Program.objects.all()
    return render(request, "ProgramPage/home.html", {"programs": programs})

def view_program(request, program_name):
    program=get_object_or_404(Program,name=program_name)
    semesters=Semester.objects.filter(program=program)
    if request.method == "POST":
        message = request.POST.get("message")
        if message:
            Feedback.objects.create(
                user=request.user if request.user.is_authenticated else None,
                message=message
            )
            messages.success(request, "Thanks for your feedback!")
            return redirect(request.path)
    return render(request,"ProgramPage/program.html",{"program":program,"semesters":semesters})



MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10 MB

@login_required
def view_semester(request, program_name, semester_name):
    semester = get_object_or_404(
        Semester,
        program__name=program_name,
        name=semester_name
    )
    subjects = Subject.objects.filter(semester=semester)
    notes = Note.objects.filter(semester=semester).select_related("subject")
    pyqs = PYQ.objects.filter(semester=semester).select_related("subject")
    note_requests = NoteRequest.objects.filter(
    semester=semester).select_related("user", "subject").order_by("-created_at")


    if request.method == "POST":
        if "upload_note" in request.POST:
            uploaded_file = request.FILES.get("file")
            title = request.POST.get("title")
            subject_id = request.POST.get("subject")

        # validations
            if not subject_id:
                messages.error(request, "Please select a subject.")
                return redirect(request.path_info)
        
            subject = get_object_or_404(Subject, id=subject_id, semester=semester)
            # Check if a file is uploaded
            if not uploaded_file:
                messages.error(request, "Please select a file to upload.")
                return redirect(request.path_info)

            # Optional: Check file size
            if uploaded_file.size > MAX_UPLOAD_SIZE:
                messages.error(request, "File too large. Max 10MB allowed.")
                return redirect(request.path_info)

            # Optional: Check file extension (PDF only)
            if not uploaded_file.name.lower().endswith(".pdf"):
                messages.error(request, "Only PDF files are allowed.")
                return redirect(
                    "view_semester",
                    program_name=program_name,
                    semester_name=semester_name
                )

            # Save to B2 bucket (django-storages handles this)
            file_hash = generate_file_hash(uploaded_file)

# Check if same file already exists
            if Note.objects.filter(file_hash=file_hash).exists():
                existing_note = Note.objects.filter(file_hash=file_hash).select_related("uploaded_by", "subject").first()

                if existing_note:
                    uploader_name = existing_note.uploaded_by.username
                    subject_name = existing_note.subject.name

                    messages.error(
                        request,
                        f"This PDF already exists under {subject_name}, uploaded by {uploader_name}."
                    )
                    return redirect(request.path_info)
                # messages.error(request, "This PDF already exists.")
                # return redirect(request.path_info)
                uploaded_file.seek(0)
            
            note = Note.objects.create(
                title=title,
                file=uploaded_file,
                semester=semester,
                file_hash=file_hash,
                subject=subject,
                uploaded_by=request.user
            )

            messages.success(request, "PDF uploaded successfully!")
            return redirect(
                "view_semester",
                program_name=program_name,
                semester_name=semester_name
            )
        # ================= PYQ UPLOAD =================
        if "upload_pyq" in request.POST:
            uploaded_file = request.FILES.get("file")
            title = request.POST.get("title")
            subject_id = request.POST.get("subject")
            if not subject_id:
                messages.error(request, "Please select a subject.")
                return redirect(request.path_info)

            subject = get_object_or_404(Subject, id=subject_id, semester=semester)

            if not uploaded_file:
                messages.error(request, "Please select a file.")
                return redirect(request.path_info)

            if uploaded_file.size > MAX_UPLOAD_SIZE:
                messages.error(request, "File too large. Max 10MB allowed.")
                return redirect(request.path_info)

            if not uploaded_file.name.lower().endswith(".pdf"):
                messages.error(request, "Only PDF files are allowed.")
                return redirect(request.path_info)

            PYQ.objects.create(
                title=title,
                file=uploaded_file,
                semester=semester,
                subject=subject,
                uploaded_by=request.user
            )

            messages.success(request, "PYQ uploaded successfully!")
            return redirect(request.path_info)
        
        if "request_note" in request.POST:
            subject_id = request.POST.get("subject")
            message = request.POST.get("message")

            if not subject_id or not message:
                messages.error(request, "Please select subject and write your requirement.")
                return redirect(request.path_info)

            subject = get_object_or_404(Subject, id=subject_id, semester=semester)

            NoteRequest.objects.create(
                user=request.user,
                semester=semester,
                subject=subject,
                message=message
            )

            messages.success(request, "Your request has been posted.")
            return redirect(request.path_info)

    return render(request, "ProgramPage/semester.html", {
        "semester": semester,
        "subjects":subjects,
        "notes": notes,
        "pyqs": pyqs,
        "note_requests": note_requests
    })

from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings
from django.core.files.storage import default_storage



@login_required
def delete_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)

    # Only staff/admin can delete
    if not request.user.is_staff:
        return HttpResponse("Unauthorized", status=403)

    note.file.delete()  # deletes PDF from media folder
    note.delete()       # deletes DB record

    return redirect(request.META.get('HTTP_REFERER', '/'))

def logout_user(request):
    logout(request)
    return redirect('auth_page')


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Feedback
import hashlib

def generate_file_hash(file):
    hash_sha256 = hashlib.sha256()
    for chunk in file.chunks():
        hash_sha256.update(chunk)
    return hash_sha256.hexdigest()

