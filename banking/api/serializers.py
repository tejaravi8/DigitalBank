from rest_framework import serializers
from banking.models import Account, Transaction


# ---------------- ACCOUNT BASIC SERIALIZER ----------------
class AccountMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            "id",
            "account_number",
            "account_type",
            "balance",
        ]


# ---------------- TRANSACTION SERIALIZER ----------------
class TransactionAPISerializer(serializers.ModelSerializer):
    account_number = serializers.CharField(
        source="account.account_number",
        read_only=True
    )
    date = serializers.DateTimeField(
        source="created_at",
        format="%Y-%m-%d %H:%M",
        read_only=True
    )

    class Meta:
        model = Transaction
        fields = [
            "id",
            "type",
            "amount",
            "party",
            "description",
            "date",            # ✅ now mapped correctly
            "account_number",
        ]


# ---------------- TRANSFER INPUT SERIALIZERS ----------------
class MobileTransferSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=15)
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)


class BankTransferSerializer(serializers.Serializer):
    to_account_number = serializers.CharField(max_length=20)
    ifsc = serializers.CharField(max_length=20)
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)


class InternalTransferSerializer(serializers.Serializer):
    from_account = serializers.CharField(max_length=20)
    to_account = serializers.CharField(max_length=20)
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)
