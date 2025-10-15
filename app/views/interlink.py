from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import pytz
from app.models import InterlinkData

@csrf_exempt
def interlink(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST allowed'}, status=405)

    try:
        data = json.loads(request.body)
        print("Raw data received JJJJJ:", data)

        # Handle array of rows or single object
        if isinstance(data, list):
            if not data:
                return JsonResponse({'error': 'Empty data array JJJJJ'}, status=400)
            entry = data[0]  # Take first row for interlink
        elif isinstance(data, dict):
            entry = data
        else:
            return JsonResponse({'error': 'Invalid data format JJJJ'}, status=400)

        # Extract fields with defaults
        date_str = entry.get('date')
        punch_no = entry.get('punchNo', '')  # can be empty
        part_model = entry.get('partModel', '')
        overall_status = entry.get('overallStatusInput', '')

        if not date_str or not part_model or not overall_status:
            return JsonResponse({'error': 'Missing required fields for interlink'}, status=400)

        print("Original date string JJJJJ:", date_str)

        # Parse the date
        try:
            date_obj = datetime.strptime(date_str, '%d/%m/%Y %I:%M:%S %p')
            timezone = pytz.timezone('Asia/Kolkata')
            date_obj_aware = timezone.localize(date_obj)
            date_obj_naive = date_obj_aware.replace(tzinfo=None)  # for SQLite/MSSQL
        except ValueError as e:
            return JsonResponse({'status': 'error', 'message': f"Invalid date format: {str(e)}"}, status=400)

        print("Timezone-aware date JJJJJ:", date_obj_aware)
        print("Naive date (without timezone JJJJJ):", date_obj_naive)
        print("INTERLINK DATA:", date_obj_naive, punch_no, part_model, overall_status)

        # Save to database
        InterlinkData.objects.create(
            Date_Time=date_obj_naive,
            PartModel=part_model,
            CompSrNo=punch_no,
            CompResultStatus=overall_status
        )

        return JsonResponse({'status': 'success', 'message': 'Interlink data saved successfully'})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
