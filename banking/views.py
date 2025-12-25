from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token

from .models import Profile, Account
from .serializers import UserSerializer


# ---------------- FRONTEND PAGES ----------------
def dashboard_page(request):
    return render(request, "banking/dashboard.html")


def profile_page(request):
    return render(request, "banking/profile.html")


def transfers_page(request):
    return render(request, "banking/transfers.html")


# def transactions_page(request):
#     return render(request, "banking/transactions.html")


def settings_page(request):
    return render(request, "banking/settings.html")


# ---------------- AUTH: REGISTER ----------------
@api_view(["POST"])
@permission_classes([AllowAny])
def register_view(request):
    data = request.data

    required_fields = ["username", "password", "phone_number"]
    for field in required_fields:
        if field not in data:
            return JsonResponse({"error": f"{field} is required"}, status=400)

    if User.objects.filter(username=data["username"]).exists():
        return JsonResponse({"error": "Username already exists"}, status=400)

    user = User.objects.create_user(
        username=data["username"],
        password=data["password"],
        email=data.get("email", "")
    )

    Profile.objects.create(
        user=user,
        phone_number=data["phone_number"]
    )

    Account.objects.create(
        user=user,
        account_number=str(user.id).zfill(10),
        account_type=data.get("account_type", "SAVINGS"),
        balance=100
    )

    token, _ = Token.objects.get_or_create(user=user)

    return JsonResponse({
        "token": token.key,
        "message": "Registration successful"
    })

# ---------------- AUTH: LOGIN ----------------
@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    data = request.data

    user = authenticate(
        username=data.get("username"),
        password=data.get("password")
    )

    if not user:
        return JsonResponse({"error": "Invalid credentials"}, status=401)

    token, _ = Token.objects.get_or_create(user=user)

    return JsonResponse({
        "token": token.key,
        "is_staff": user.is_staff,
        "username": user.username
    })



# ---------------- AUTH: ME ----------------
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me_view(request):
    serializer = UserSerializer(request.user)
    return JsonResponse(serializer.data, safe=False)


# ---------------- PROFILE UPDATE ----------------
@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_profile(request):
    user = request.user
    profile = user.profile
    data = request.data

    # User model fields
    user.first_name = data.get("first_name", user.first_name)
    user.last_name = data.get("last_name", user.last_name)
    user.email = data.get("email", user.email)
    user.save()

    # Profile model fields
    profile.phone_number = data.get("phone_number", profile.phone_number)
    profile.address = data.get("address", profile.address)
    profile.save()

    return JsonResponse({"message": "Profile updated successfully"})


# ---------------- PROFILE ACCESS RULES ----------------
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def profile_access(request):
    profile = request.user.profile

    return JsonResponse({
        "kyc_status": profile.kyc_status,
        "operation_access": profile.kyc_status == "approved"
    })
