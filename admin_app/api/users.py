import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

@csrf_exempt
@staff_member_required
@require_POST
def toggle_user_status(request):
    data = json.loads(request.body)
    user_id = data.get("user_id")

    try:
        user = User.objects.get(id=user_id)
        if user.is_superuser:
            return JsonResponse(
        {"error": "Superuser account cannot be deactivated"},
        status=403
    )
        user.is_active = not user.is_active
        user.save()

        return JsonResponse({
            "message": "User status updated",
            "is_active": user.is_active
        })

    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)
