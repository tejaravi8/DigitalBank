from decimal import Decimal
from django.db import transaction as db_transaction
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from banking.models import Account, Transaction, Profile
from banking.api.serializers import (
    BankTransferSerializer,
    InternalTransferSerializer,
    MobileTransferSerializer
)

# ---------------- SEND TO BANK ACCOUNT ----------------
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def send_to_account(request):
    serializer = BankTransferSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    amount = Decimal(serializer.validated_data["amount"])
    to_account_number = serializer.validated_data["to_account_number"]
    ifsc = serializer.validated_data["ifsc"]

    # 🔐 KYC CHECK
    if request.user.profile.kyc_status != "approved":
        return JsonResponse({"error": "KYC not approved"}, status=403)

    try:
        with db_transaction.atomic():
            from_account = (
                Account.objects
                .select_for_update()
                .filter(user=request.user)
                .first()
            )

            if not from_account:
                return JsonResponse({"error": "Sender account not found"}, status=404)

            to_account = (
                Account.objects
                .select_for_update()
                .get(account_number=to_account_number, ifsc_code=ifsc)
            )

            if from_account.balance < amount:
                return JsonResponse({"error": "Insufficient balance"}, status=400)

            # 💸 BALANCE UPDATE
            from_account.balance -= amount
            to_account.balance += amount
            from_account.save()
            to_account.save()

            # 🧾 TRANSACTIONS
            Transaction.objects.create(
                user=request.user,
                account=from_account,
                type="debit",
                amount=amount,
                party=to_account.account_number,
                description="Bank transfer",
            )

            Transaction.objects.create(
                user=to_account.user,
                account=to_account,
                type="credit",
                amount=amount,
                party=from_account.account_number,
                description="Bank transfer received",
            )

        return JsonResponse({"message": "Bank transfer successful"})

    except Account.DoesNotExist:
        return JsonResponse({"error": "Invalid account details"}, status=404)


# ---------------- SEND TO MOBILE ----------------
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def send_to_mobile(request):
    serializer = MobileTransferSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    amount = Decimal(serializer.validated_data["amount"])
    mobile = serializer.validated_data["mobile"]

    if request.user.profile.kyc_status != "approved":
        return JsonResponse({"error": "KYC not approved"}, status=403)

    try:
        receiver_profile = Profile.objects.get(phone_number=mobile)

        with db_transaction.atomic():
            sender_account = (
                Account.objects
                .select_for_update()
                .filter(user=request.user)
                .first()
            )

            receiver_account = (
                Account.objects
                .select_for_update()
                .filter(user=receiver_profile.user)
                .first()
            )

            if not sender_account or not receiver_account:
                return JsonResponse({"error": "Account not found"}, status=404)

            if sender_account.balance < amount:
                return JsonResponse({"error": "Insufficient balance"}, status=400)

            sender_account.balance -= amount
            receiver_account.balance += amount
            sender_account.save()
            receiver_account.save()

            Transaction.objects.create(
                user=request.user,
                account=sender_account,
                type="debit",
                amount=amount,
                party=mobile,
                description="Mobile transfer",
            )

            Transaction.objects.create(
                user=receiver_profile.user,
                account=receiver_account,
                type="credit",
                amount=amount,
                party=request.user.username,
                description="Mobile transfer received",
            )

        return JsonResponse({"message": "Mobile transfer successful"})

    except Profile.DoesNotExist:
        return JsonResponse({"error": "Receiver not found"}, status=404)



# ---------------- INTERNAL ACCOUNT TRANSFER ----------------
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def transfer_between_accounts(request):
    serializer = InternalTransferSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    from_acc_no = serializer.validated_data["from_account"]
    to_acc_no = serializer.validated_data["to_account"]
    amount = Decimal(serializer.validated_data["amount"])

    if from_acc_no == to_acc_no:
        return JsonResponse({"error": "Same account transfer not allowed"}, status=400)

    try:
        with db_transaction.atomic():

            from_account = (
                Account.objects
                .select_for_update()
                .get(account_number=from_acc_no, user=request.user)
            )

            to_account = (
                Account.objects
                .select_for_update()
                .get(account_number=to_acc_no, user=request.user)
            )

            if from_account.balance < amount:
                return JsonResponse({"error": "Insufficient balance"}, status=400)

            from_account.balance -= amount
            to_account.balance += amount
            from_account.save()
            to_account.save()

            Transaction.objects.create(
                user=request.user,
                account=from_account,
                type="debit",
                amount=amount,
                party=to_account.account_number,
                description="Internal transfer",
            )

            Transaction.objects.create(
                user=request.user,
                account=to_account,
                type="credit",
                amount=amount,
                party=from_account.account_number,
                description="Internal transfer",
            )

        return JsonResponse({"message": "Internal transfer successful"})

    except Account.DoesNotExist:
        return JsonResponse({"error": "Invalid account selection"}, status=404)



# ---------------- PLACEHOLDERS ----------------
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def request_money_coming(request):
    return JsonResponse({"message": "Request money feature coming soon"})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def standing_instructions_coming(request):
    return JsonResponse({"message": "Standing instructions feature coming soon"})
