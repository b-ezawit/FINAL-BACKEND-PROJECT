from django.urls import path
from . import views

urlpatterns = [
    # Scan Lifecycle routes
    path('scan/start', views.start_scan, name='start_scan'),
    path('scan/status/<uuid:job_id>', views.check_status, name='check_status'),
    path('scan/result/<uuid:job_id>', views.get_results, name='get_results'),
    path('scan/cancel/<uuid:job_id>', views.cancel_job, name='cancel_job'),
    path('scan/remove/<uuid:job_id>', views.remove_job_data, name='remove_job_data'),
    
    # Global dashboard lists
    path('jobs/jobs', views.list_all_jobs, name='list_all_jobs'),
]