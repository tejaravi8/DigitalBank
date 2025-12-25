from django.db import models
from django.contrib.auth.models import User


# ---------------- PROFILE ----------------
class Profile(models.Model):
    KYC_STATUS = (
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    phone_number = models.CharField(max_length=15)
    address = models.TextField(blank=True, null=True)
    kyc_status = models.CharField(max_length=20, choices=KYC_STATUS, default="pending")

    def __str__(self):
        return self.user.username


# ---------------- ACCOUNT ----------------

class Account(models.Model):
    ACCOUNT_TYPES = (
        ("SAVINGS", "Savings"),
        ("CURRENT", "Current"),
        ("SYSTEM", "System"),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="accounts",
        null=True,
        blank=True
    )

    account_number = models.CharField(max_length=30, unique=True)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES)
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    # 🔑 IMPORTANT FLAG
    is_system_account = models.BooleanField(default=False)

    branch_name = models.CharField(max_length=100, default="Main Branch")
    ifsc_code = models.CharField(max_length=20, default="DIGI000123")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.account_number



# ---------------- TRANSACTION ----------------
class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ("credit", "Credit"),
        ("debit", "Debit"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)

    type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)

    party = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)

    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.type} - {self.amount}"
