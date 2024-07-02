from django.http import JsonResponse
from builds.models import Builds

from backend.map_json import get_map_json
from backend.macro_details_json import get_macro_details_json
from backend.micro_details_json import get_micro_details_json

def get_json(request):
     build_id = request.GET.get('build_id')
     extra_work = request.GET.get('extra_work')
     json_data = get_macro_details_json(int(build_id), int(extra_work))
     return JsonResponse(json_data, safe=False)

def get_micro_details_json_view(request):
     build_id = request.GET.get('build_id')
     build = Builds.objects.get(pk = int(build_id))
     json_data = get_micro_details_json(build)
     return JsonResponse(json_data, safe=False)

def map_json(request):
     json_data = get_map_json(1)
     return JsonResponse(json_data, safe=False)

