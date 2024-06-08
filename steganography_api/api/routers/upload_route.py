import magic
from pathlib import Path

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.files import File

from ..models import FileModel
from ..utils.is_valid_file import is_valid_file

@csrf_exempt
def upload_file(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'ERROR'}, status=404)

    try:
        # Handle only one file
        if len(request.FILES) <= 0:
            return JsonResponse({'status': 'NO_FILE'}, status=400)
        elif len(request.FILES) >= 2:
            return JsonResponse({'status': 'ONLY_ONE_FILE_ALLOWED'}, status=400)

        uploaded_file = list(request.FILES.values())[0]

        # Check if file is too large
        # (2 MB)
        max_file_size = 2 * 1024 * 1024 
        if uploaded_file.size > max_file_size:
            return JsonResponse({'status': 'FILE_TOO_LARGE'}, status=400)

        # Use magic to determine file type from file content...
        file_content = uploaded_file.read()
        mime = magic.Magic(mime=True)
        file_type = mime.from_buffer(file_content)
        print(file_type)
        if not is_valid_file(file_type):
            return JsonResponse({'status': 'INVALID_FILE_TYPE'}, status=400)
        uploaded_file.seek(0)

        # Create the file instance
        file_instance = FileModel(
            file_type=file_type,
            file_name=uploaded_file.name
        )
        file_instance.save()

        # Save the uploaded file to the appropriate path
        file_instance.file.save(uploaded_file.name, uploaded_file)
        file_instance.save()

        return JsonResponse({'status': 'OK', 'uuid': file_instance.id}, status=200)
    except Exception as e:
        print(f"Error occurred uploading file :: {e}", flush=True)
        return JsonResponse({'status': 'ERROR', 'message': str(e)}, status=500)