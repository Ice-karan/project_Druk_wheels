from django.shortcuts import render,get_object_or_404,redirect
from item.models import Item, Category
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import CategoryForm  # Importing the CategoryForm

# View for rendering the dashboard index page
@login_required
def index(request):
    # Get items created by the current user
    items = Item.objects.filter(created_by=request.user)
    # Get all users
    all_users = User.objects.all()
    # Get all categories
    categories = Category.objects.all()

    # Render the dashboard index page with necessary context
    return render(request, 'dashboard/index.html', {
        'items': items,
        'all_users': all_users,
        'categories': categories,
    })

# View for deleting users
@login_required
def deleteUsers(request):
    if request.method == 'POST':
        # Get the user ID from the request
        user_id = request.POST.get('user_id')
        # Get the user object
        user = get_object_or_404(User, id=user_id)
        # Delete the user
        user.delete()
    return redirect('dashboard:index')  # Redirect to the dashboard index page after deletion

# View for promoting/demoting users
@login_required
def promoteUser(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return redirect('dashboard:index')  # Redirect to the dashboard index page if the user doesn't exist

    # Toggle the user's staff and superuser status
    user.is_staff = not user.is_staff
    user.is_superuser = not user.is_superuser
    user.save()
    return redirect('dashboard:index')  # Redirect to the dashboard index page after promoting/demoting the user

# View for adding a new category
@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard:index')
    else:
        form = CategoryForm()

    # Get all categories
    categories = Category.objects.all()
    # Render the add category page with necessary context
    return render(request, 'dashboard/add_category.html', {
        'form': form,
        'categories': categories,
    })
