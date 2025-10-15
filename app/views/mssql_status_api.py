from django.http import JsonResponse
from mini_soft.utils import get_mssql_status
import sys

def mssql_status_api(request):
    status = get_mssql_status()
    print(f"[API] {status['status']}", file=sys.stdout, flush=True)  # 👈 prints in terminal
    return JsonResponse(status)
