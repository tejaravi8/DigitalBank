from decimal import Decimal
from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required

from banking.models import Account, Transaction


@csrf_exempt
@staff_member_required
@require_POST
def credit_user_account(request):
    """
    Admin deposits money into a user's bank account
    Source of funds: Bank Pool (system account)
    """

    account_number = request.POST.get("account_number")
    amount = request.POST.get("amount")

    # ---------- VALIDATION ----------
    if not account_number or not amount:
        return JsonResponse(
            {"error": "Account number and amount are required"},
            status=400
        )

    try:
        amount = Decimal(amount)
    except:
        return JsonResponse({"error": "Invalid amount"}, status=400)

    if amount <= 0:
        return JsonResponse({"error": "Amount must be greater than zero"}, status=400)

    try:
        # ---------- BANK POOL ----------
        bank_pool = Account.objects.filter(is_system_account=True).first()
        if not bank_pool:
            return JsonResponse({"error": "Bank pool account not found"}, status=500)

        if bank_pool.balance < amount:
            return JsonResponse({"error": "Insufficient bank funds"}, status=400)

        # ---------- USER ACCOUNT ----------
        user_account = Account.objects.select_for_update().get(
            account_number=account_number
        )

        if not user_account.user.is_active:
            return JsonResponse({"error": "User account is inactive"}, status=403)

        # ---------- ATOMIC TRANSACTION ----------
        with transaction.atomic():
            bank_pool.balance -= amount
            bank_pool.save()

            user_account.balance += amount
            user_account.save()

            Transaction.objects.create(
                user=user_account.user,
                account=user_account,
                amount=amount,
                type="credit",
                party="BANK",
                description="Admin deposit from Bank Pool"
            )

        return JsonResponse({
            "message": "Deposit successful",
            "credited_amount": str(amount),
            "account_number": user_account.account_number,
            "new_balance": str(user_account.balance)
        })

    except Account.DoesNotExist:
        return JsonResponse({"error": "Account not found"}, status=404)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
