from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.http import JsonResponse
import json

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def get_contenttype_model_choices(request):
    try:
        data = request.body.decode('utf-8')
        data = json.loads(data)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    

    content_type_id = data.get("content_type_id")
    
    content_type = ContentType.objects.filter(id=content_type_id).first()
    
    if not content_type:
        return JsonResponse({"error": "ContentType not found"}, status=404)
    
    model_class = content_type.model_class()
    
    objects = [
        {"id": obj.id, "str": str(obj)}
        for obj in model_class.objects.all()
    ]
    
    return JsonResponse(objects, safe=False)