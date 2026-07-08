from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import ExtractionJob

@api_view(['POST'])
def start_scan(request):
    token = request.data.get('token')
    if not token:
        return Response(
            {"error": "Invalid or missing API token provided."}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    job = ExtractionJob.objects.create(status='PENDING')
    
    return Response(
        {
            "job_id": str(job.job_id),
            "status": job.status,
            "message": "Extraction job successfully initiated."
        }, 
        status=status.HTTP_202_ACCEPTED
    )

@api_view(['GET'])
def check_status(request, job_id):
    job = get_object_or_404(ExtractionJob, pk=job_id)
    
    return Response({
        "job_id": str(job.job_id),
        "status": job.status,
        "record_count": job.record_count,
        "created_at": job.created_at
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_results(request, job_id):
    job = get_object_or_404(ExtractionJob, pk=job_id)
    
    if job.status in ['PENDING', 'IN_PROGRESS']:
        return Response(
            {"error": "Job is still processing. Results are not ready yet."},
            status=status.HTTP_400_BAD_REQUEST
        )
        
    return Response({
        "job_id": str(job.job_id),
        "status": job.status,
        "results": job.extracted_data
    }, status=status.HTTP_200_OK)

@api_view(['POST'])
def cancel_job(request, job_id):
    job = get_object_or_404(ExtractionJob, pk=job_id)
    
    if job.status in ['COMPLETED', 'FAILED', 'CANCELLED']:
        return Response(
            {"error": f"Cannot cancel job in {job.status} state."},
            status=status.HTTP_400_BAD_REQUEST
        )
        
    job.status = 'CANCELLED'
    job.save() 
    
    return Response({"message": "Job successfully cancelled."}, status=status.HTTP_200_OK)

@api_view(['DELETE'])
def remove_job_data(request, job_id):
    job = get_object_or_404(ExtractionJob, pk=job_id)
    
    job.delete()
    
    return Response({"message": "Job data removed successfully."}, status=status.HTTP_200_OK)

@api_view(['GET'])
def list_all_jobs(request):
    jobs = ExtractionJob.objects.all()
    
    jobs_list = []
    for job in jobs:
        jobs_list.append({
            "job_id": str(job.job_id),
            "status": job.status,
            "record_count": job.record_count
        })
        
    return Response(jobs_list, status=status.HTTP_200_OK)