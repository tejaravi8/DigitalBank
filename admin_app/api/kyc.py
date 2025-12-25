from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_POST

from banking.models import Profile


@staff_member_required
@require_POST
def update_kyc_status(request):
    user_id = request.POST.get("user_id")
    action = request.POST.get("action")

    if not user_id or not action:
        return JsonResponse(
            {"error": "Invalid request"},
            status=400
        )

    try:
        profile = Profile.objects.get(user_id=user_id)
    except Profile.DoesNotExist:
        return JsonResponse(
            {"error": "Profile not found"},
            status=404
        )

    if action == "approve":
        profile.kyc_status = "approved"
    elif action == "reject":
        profile.kyc_status = "rejected"
    else:
        return JsonResponse(
            {"error": "Invalid action"},
            status=400
        )

    profile.save()

    return JsonResponse({
        "message": f"KYC {action}d successfully"
    })
