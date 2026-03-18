from django.urls import path
from .import views


urlpatterns = [
    path('', views.auth_page, name='login'),
    path('login/', views.auth_page, name='login'),
    # path('homepage/',views.home,name='home'),
    path('auth-page/', views.auth_page, name='auth_page'),
    # path('logout/', views.logout_user, name='logout'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('complete-registration/', views.complete_registration, name='complete_registration'),
    # path("program/<str:program_name>/", views.view_program, name="view_program"),
    # path("program/<str:program_name>/<str:semester_name>/", views.view_semester, name="view_semester"),
    # path('delete-note/<int:note_id>/', views.delete_note, name='delete_note'),
    path("pdfjs/<int:note_id>/", views.pdf_viewer, name="pdf_js_viewer"),
    path("pdfjs/<int:note_id>/file/", views.serve_pdf, name="serve_pdf"),
    path("pdfjs/<int:note_id>/ai/", views.pdf_ai_tools, name="pdf_ai_tools"),

]
