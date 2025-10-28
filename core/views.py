from django.shortcuts import render, redirect
from item.models import Category, Item
from django.contrib.auth import logout, login
from .forms import SignupForm
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

def index(request):
    # Retrieve the first 6 items that are not sold
    items = Item.objects.filter(is_sold=False)[0:6]
    # Retrieve all categories
    categories = Category.objects.all()
    # Render the 'core/index.html' template with the context containing items and categories
    return render(request, 'core/index.html', {
        'categories': categories,
        'items': items,
    })

def contact(request):
    # Render the 'core/contact.html' template
    return render(request, 'core/contact.html')

def signup(request):
    if request.method == 'POST':
        # Initialize the signup form with POST data
        form = SignupForm(request.POST)
        
        if form.is_valid():
            # Save the new user object without committing to the database yet
            user = form.save(commit=False)
            # Normalize the email and username to lowercase
            user.email = form.cleaned_data['email'].lower()
            user.username = form.cleaned_data['username'].lower()
            # Save the user object to the database
            user.save()
            # Log the user in
            login(request, user)
            # Redirect to the login page after successful signup
            return redirect('/login/')
    else:
        # Initialize an empty signup form if the request method is not POST
        form = SignupForm()

    # Render the 'core/signup.html' template with the signup form
    return render(request, 'core/signup.html', {
        'form': form,
    })

def logout_view(request):
    # Log the user out
    logout(request)
    # Redirect to the login page after logging out
    return redirect('/login/')  # Replace '/login/' with the name of the URL pattern for your home page if necessary


class CustomTokenObtainPairView(TokenObtainPairView):
    pass


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Successfully logged out."}, status=205)
        except Exception as e:
            return Response({"error": "Bad request"}, status=400)
