# Testing route...
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

@csrf_exempt
def ping(request):
    if request.method != 'GET':
        return JsonResponse({'status': 'ERROR'}, status=404)
    return JsonResponse({'status': 'OK'}, status=200)