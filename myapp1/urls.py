from django.urls import path
from . import views
#from django.contrib.auth.views import LogoutView
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path("dashboard/", views.dashboard, name="dashboard"),

    path("add/", views.add_incident, name="add_incident"),
    path("edit/<int:id>/", views.edit_incident, name="edit_incident"),
    path("delete/<int:id>/", views.delete_incident, name="delete_incident"),
    path('logout/', views.logout, name='logout'),
    path('incident/<int:id>/history/', views.incident_history, name='incident_history'),


    path('reports/', views.report_list, name='reports'),
    path('reports/<int:incident_id>/', views.report_details, name='report_detail'),

    # urls.py
    path('history/', views.incident_history, name='incident_history'),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)