from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from ..models import FileModel

def find_encoded_files(file_model):
    # Query files whose encoded_from field matches the given FileModel instance
    encoded_files = FileModel.objects.filter(encoded_from=file_model)
    return encoded_files

def get_related_files_data(request):
    if request.method != 'GET':
        return JsonResponse({'status': 'ERROR'}, status=405)

    try:
        file_uuid = request.GET['file_uuid']
        file_model = get_object_or_404(FileModel, id=file_uuid)
        # Find files whose encoded_from field matches the given UUID
        encoded_files = find_encoded_files(file_model)
        
        data = []

        # Append parent if exists
        if file_model.encoded_from != None:
            file = file_model.encoded_from

            original_encoded_id = None
            if file.encoded_from != None:
                original_encoded_id = file.encoded_from.id
            data.append({
                "uuid": file.id,
                "name": file.file_name,
                "type": file.file_type,
                "parent": original_encoded_id,
                "created_at": file.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                "relation": "parent"
            })

        # Append all childs
        for file in encoded_files:
            data.append({
                "uuid": file.id,
                "name": file.file_name,
                "type": file.file_type,
                "parent": file_uuid,
                "created_at": file.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                "relation": "child"
            })
        
        return JsonResponse({'data': data, "status": "SUCCESS"}, status=200)
    except Exception as e:
        error_message = f"Error occurred finding encoded files: {e}"
        print(error_message, flush=True)
        return JsonResponse({'status': 'ERROR', 'message': error_message}, status=500)
