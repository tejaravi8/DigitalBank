from django.contrib import admin
from .models import Profile, Account, Transaction


# ---------------- PROFILE ADMIN ----------------
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "phone_number", "kyc_status")
    list_filter = ("kyc_status",)
    search_fields = ("user__username", "phone_number")


# ---------------- ACCOUNT ADMIN ----------------
@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = (
        "account_number",
        "user",
        "account_type",
        "balance",
        "branch_name",
        "ifsc_code",
        "created_at",
    )
    search_fields = ("account_number", "user__username")
    list_filter = ("account_type", "branch_name")
    readonly_fields = ("created_at",)


# ---------------- TRANSACTION ADMIN ----------------
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "account",
        "type",
        "amount",
        "party",
        "date",
    )
    list_filter = ("type", "date")
    search_fields = ("user__username", "account__account_number")
    readonly_fields = ("date",)
