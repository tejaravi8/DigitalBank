from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.db.models import Sum
from banking.models import Transaction, Account

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def dashboard_summary(request):
    user = request.user

    # 💰 Balance
    balance = (
        Account.objects
        .filter(user=user)
        .aggregate(total=Sum("balance"))["total"] or 0
    )

    # 💸 Totals
    total_deposits = (
        Transaction.objects
        .filter(user=user, type="credit")
        .aggregate(total=Sum("amount"))["total"] or 0
    )

    total_withdrawals = (
        Transaction.objects
        .filter(user=user, type="debit")
        .aggregate(total=Sum("amount"))["total"] or 0
    )

    transaction_count = Transaction.objects.filter(user=user).count()

    # 📈 Chart data (last 7 transactions)
    recent = (
        Transaction.objects
        .filter(user=user)
        .order_by("-date")[:7][::-1]
    )

    labels = [tx.date.strftime("%d %b") for tx in recent]
    credits = [float(tx.amount) if tx.type == "credit" else 0 for tx in recent]
    debits = [float(tx.amount) if tx.type == "debit" else 0 for tx in recent]

    return JsonResponse({
        "balance": float(balance),
        "total_deposits": float(total_deposits),
        "total_withdrawals": float(total_withdrawals),
        "transaction_count": transaction_count,
        "chart": {
            "labels": labels,
            "credits": credits,
            "debits": debits
        }
    })
