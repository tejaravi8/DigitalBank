import csv
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required

from banking.models import Transaction


@staff_member_required
def export_transactions_csv(request):
    """
    Export all transactions as CSV
    """

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="transactions_report.csv"'

    writer = csv.writer(response)

    # CSV HEADER
    writer.writerow([
        "Date",
        "Account Number",
        "Username",
        "Type",
        "Amount",
        "Party",
        "Description"
    ])

    transactions = (
        Transaction.objects
        .select_related("account", "account__user")
        .order_by("-date")
    )

    for t in transactions:
        writer.writerow([
            t.date.strftime("%Y-%m-%d %H:%M"),
            t.account.account_number,
            "BANK" if t.account.is_system_account else t.account.user.username,
            t.type.upper(),
            t.amount,
            t.party or "",
            t.description or ""
        ])

    return response


from django.contrib.auth.models import User
from banking.models import Account, Transaction
import csv
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required


@staff_member_required
def export_users_csv(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="users_report.csv"'

    writer = csv.writer(response)
    writer.writerow([
        "Username",
        "Email",
        "Phone",
        "KYC Status",
        "Date Joined"
    ])

    for u in User.objects.all():
        profile = getattr(u, "profile", None)
        writer.writerow([
            u.username,
            u.email,
            profile.phone_number if profile else "",
            profile.kyc_status if profile else "",
            u.date_joined.strftime("%Y-%m-%d")
        ])

    return response

@staff_member_required
def export_accounts_csv(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="accounts_report.csv"'

    writer = csv.writer(response)
    writer.writerow([
        "Account Number",
        "Username",
        "Type",
        "Balance",
        "IFSC",
        "Branch"
    ])

    for acc in Account.objects.select_related("user"):
        writer.writerow([
            acc.account_number,
            "BANK" if acc.is_system_account else acc.user.username,
            acc.account_type,
            acc.balance,
            acc.ifsc_code,
            acc.branch_name
        ])

    return response
