from django.urls import path
from .import views
urlpatterns = [
    path('homepage/',views.home,name='home'),
    path('logout/', views.logout_user, name='logout'),
    path('delete-note/<int:note_id>/', views.delete_note, name='delete_note'),
    path("program/<str:program_name>/", views.view_program, name="view_program"),
    path("program/<str:program_name>/<str:semester_name>/", views.view_semester, name="view_semester"),
]

