from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from banking.models import Account, Transaction, Profile
from django.db.models import Sum
import json
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
# from django.http import HttpResponse



@staff_member_required
def admin_dashboard(request):
    total_users = User.objects.count()
    total_accounts = Account.objects.count()
    total_transactions = Transaction.objects.count()

    # Bank Pool Account balance
    bank_pool = Account.objects.filter(is_system_account=True).first()
    bank_balance = bank_pool.balance if bank_pool else 0

    context = {
        "total_users": total_users,
        "total_accounts": total_accounts,
        "total_transactions": total_transactions,
        "bank_balance": bank_balance,
    }

    return render(request, "admin_app/dashboard.html", context)

@staff_member_required
def kyc_page(request):
    profiles = Profile.objects.filter(kyc_status="pending").select_related("user")
    return render(request, "admin_app/kyc.html", {
        "profiles": profiles
    })
    
    
@staff_member_required
def users_page(request):
    users = (
        User.objects
        .select_related("profile")
        .all()
    )
    return render(request, "admin_app/users.html", {
        "users": users
    })

@staff_member_required
def accounts_page(request):
    accounts = Account.objects.select_related("user").order_by("-created_at")

    return render(
        request,
        "admin_app/accounts.html",
        {"accounts": accounts}
    )

@staff_member_required
def transactions_page(request):
    transactions = (
        Transaction.objects
        .select_related("account", "account__user")
        .order_by("-date")
    )

    return render(
        request,
        "admin_app/transactions.html",
        {"transactions": transactions}
    )
    
@staff_member_required
def reports_page(request):
    return render(request,"admin_app/reports.html",)

@csrf_exempt
@staff_member_required
def remove_user(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid method"}, status=405)

    data = json.loads(request.body)
    user_id = data.get("user_id")

    user = User.objects.get(id=user_id)
    user.is_active = False
    user.save()

    return JsonResponse({"message": "User removed"})
    
    
@csrf_exempt
@staff_member_required
def reactivate_user(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid method"}, status=405)

    data = json.loads(request.body)
    user_id = data.get("user_id")

    try:
        user = User.objects.get(id=user_id)

        user.is_active = True
        user.save()

        # Reactivate accounts (optional rule)
        user.account_set.update(is_active=True)

        return JsonResponse({
            "message": "User reactivated successfully"
        })

    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)
    
    
@staff_member_required
def admin_user_details(request):
    user_id = request.GET.get("user")

    user = User.objects.select_related("profile").get(id=user_id)
    accounts = Account.objects.filter(user=user)

    data = {
        "user": {
            "username": user.username,
            "email": user.email,
            "phone": user.profile.phone_number,
            "address": user.profile.address,
            "kyc_status": user.profile.kyc_status,
            "is_active": user.is_active,
        },
        "accounts": [
            {
                "account_number": acc.account_number,
                "account_type": acc.account_type,
                "ifsc_code": acc.ifsc_code,
                "branch_name": acc.branch_name,
                "balance": acc.balance,
                "created_at": acc.created_at.strftime("%Y-%m-%d"),
            }
            for acc in accounts
        ]
    }

    return JsonResponse(data)

@csrf_exempt
@staff_member_required
@require_POST
def delete_user_permanently(request):
    data = json.loads(request.body)
    user_id = data.get("user_id")

    try:
        user = User.objects.get(id=user_id)

        # 🔴 SAFETY CHECK: do not delete superadmin
        if user.is_superuser:
            return JsonResponse(
                {"error": "Super admin cannot be deleted"},
                status=403
            )

        user.delete()

        return JsonResponse({
            "message": "User permanently deleted"
        })

    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)