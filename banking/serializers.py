from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profile, Account, Transaction


# ---------------- PROFILE SERIALIZER ----------------
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            "phone_number",
            "address",
            "kyc_status",
        ]


# ---------------- ACCOUNT SERIALIZER ----------------
class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            "id",
            "account_number",
            "account_type",
            "balance",
            "branch_name",
            "ifsc_code",
            "created_at",
        ]


# ---------------- USER SERIALIZER ----------------
class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    accounts = AccountSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "profile",
            "accounts",
        ]


# ---------------- TRANSACTION SERIALIZER ----------------
class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            "id",
            "type",
            "amount",
            "party",
            "description",
            "date",
        ]
