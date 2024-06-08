from django.http import FileResponse, JsonResponse
from django.shortcuts import get_object_or_404
from ..models import FileModel

def download_file(request):
    if request.method != 'GET':
        return JsonResponse({'status': 'ERROR'}, status=404)

    try:
        file_uuid = request.GET['file_uuid']
        file_model = get_object_or_404(FileModel, id=file_uuid)
        file = file_model.file
        response = FileResponse(file)
        response['Content-Disposition'] = 'attachment; filename=' + file_model.file_name
        return response
    except Exception as e:
        print(f"Error occurred downloading file :: {e}", flush=True)
        return JsonResponse({'status': 'ERROR'}, status=500)
