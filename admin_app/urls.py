from django.urls import path
from .views import admin_dashboard,kyc_page,users_page,accounts_page,transactions_page,reports_page
from .api.credit import credit_user_account
from .api.kyc import update_kyc_status
from .views import admin_user_details,delete_user_permanently
from .api.reports import export_transactions_csv
from .api.users import toggle_user_status
from .api.reports import (
    export_transactions_csv,
    export_users_csv,
    export_accounts_csv
)

urlpatterns = [
    path("dashboard/", admin_dashboard),
    path("kyc/", kyc_page),
    path("users/", users_page),
    path("accounts/", accounts_page),
    path("transactions/", transactions_page),
     path("reports/", reports_page),
    
    path("api/credit/", credit_user_account),
    path("api/kyc/", update_kyc_status),
    path("api/reports/transactions/", export_transactions_csv),
    path("api/reports/transactions/", export_transactions_csv),
    path("api/reports/users/", export_users_csv),
    path("api/reports/accounts/", export_accounts_csv),
    path("api/users/toggle/", toggle_user_status),
    path("api/user-details/", admin_user_details),
    path("api/users/delete/", delete_user_permanently),


]
