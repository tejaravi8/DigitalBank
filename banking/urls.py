from django.urls import path
from .views import (
    register_view, login_view, me_view, update_profile, profile_access,
    dashboard_page, profile_page, transfers_page, settings_page ,  #transactions_page
)
from banking.api.transfers import (
    send_to_mobile, send_to_account, transfer_between_accounts,
    request_money_coming, standing_instructions_coming
)
from banking.api.dashboard import dashboard_summary

urlpatterns = [

    # ---------------- AUTH ----------------
    path("auth/register/", register_view),
    path("auth/login/", login_view),
    path("auth/me/", me_view),

    # ---------------- PROFILE ----------------
    path("profile/update/", update_profile),
    path("profile/access/", profile_access),

    # ---------------- FRONTEND PAGES ----------------
    path("dashboard/", dashboard_page),
    path("profile/", profile_page),
    path("transfers/", transfers_page),
    path("settings/", settings_page),

    # ---------------- TRANSFERS API ----------------
    path("transfers/mobile/", send_to_mobile),
    path("transfers/account/", send_to_account),
    path("transfers/internal/", transfer_between_accounts),
    path("transfers/request/", request_money_coming),
    path("transfers/standing/", standing_instructions_coming),


    path("dashboard/summary/", dashboard_summary),

]
