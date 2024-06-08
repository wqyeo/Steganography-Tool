from django.http import JsonResponse
from ..models import FileModel

def fetch_latest_files(top=25):
    latest_files = FileModel.objects.order_by('-created_at')[:top]
    return latest_files

def get_recent_files_data(request):
    if request.method != 'GET':
        return JsonResponse({'status': 'ERROR'}, status=404)

    try:
        latest_files = fetch_latest_files()
        data = []
        for file in latest_files:
            original_encoded_id = None
            if file.encoded_from != None:
                original_encoded_id = file.encoded_from.id

            data.append({
                "uuid": file.id,
                "name": file.file_name,
                "type": file.file_type,
                "parent": original_encoded_id,
                "created_at": file.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            })
        return JsonResponse({'data': data, "status": "SUCCESS"}, status=200)
    except Exception as e:
        print(f"Error occurred fetching latest files :: {e}", flush=True)
        return JsonResponse({'status': 'ERROR'}, status=500)
