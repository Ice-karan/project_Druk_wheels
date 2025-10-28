from django.shortcuts import render,get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import NewItemForm, EditItemForm  # Importing necessary forms
from .models import Item, Category  # Importing Item and Category models

from django.db.models import Q  # Importing Q for complex queries

# View for displaying items
def items(request):
    # Get the 'query' parameter from the URL, default to empty string
    query = request.GET.get('query','')
    # Get all items that are not sold
    items = Item.objects.filter(is_sold=False)
    # Get all categories
    categories = Category.objects.all()
    # Get the 'category' parameter from the URL, default to 0
    category_id = request.GET.get('category',0)

    # If category_id is provided, filter items by that category
    if category_id:
        items = items.filter(category_id=category_id)

    # If query is provided, filter items by name or description containing the query
    if query:
        items = items.filter(Q(name__icontains=query)|
                             Q(description__icontains=query))
    
    # Render the items page with necessary context
    return render(request, 'item/items.html',{
        'items':items,
        'query':query,
        'categories':categories,
        'category_id':int(category_id),
    })

# View for displaying item details
def detail(request, pk):
    # Get the item by its primary key (pk)
    item = get_object_or_404(Item, pk=pk)
    # Get related items (items in the same category excluding the current item)
    related_items = Item.objects.filter(category=item.category).exclude(pk=pk)[:3]

    # Clean up the color field, removing unnecessary characters
    if item.color:
        item.color = item.color.replace(',', ' ')
        item.color = item.color.replace('[', '')
        item.color = item.color.replace(']', '')
        item.color = item.color.replace("'", '')

    # Render the item detail page with necessary context
    return render(request, 'item/detail.html',{
        'item':item,
        'related_items':related_items,
    })

# View for creating a new item
@login_required
def new(request):
    if request.method == 'POST':
        form = NewItemForm(request.POST, request.FILES)
        
        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()

            return redirect('item:detail', pk=item.id)

    else:
        form = NewItemForm(initial={'category': 'default_category_value'})  # Set initial category value
    categories = Category.objects.all()  # Get all categories

    # Render the new item form with necessary context
    return render(request, 'item/form.html',{
        'form':form,
        'title':'New item',
        'categories':categories,
    })

# View for editing an existing item
@login_required
def edit(request, pk):
    # Get the item by its primary key (pk) and the user who created it
    item = get_object_or_404(Item, pk=pk,created_by=request.user)

    if request.method == 'POST':
        form = EditItemForm(request.POST, request.FILES, instance=item)

        if form.is_valid():
            form.save()

            return redirect('item:detail', pk=item.id)

    else:
        form = EditItemForm(instance=item)

    # Render the edit item form with necessary context
    return render(request, 'item/form.html',{
        'form':form,
        'title':'Edit item',
    })

# View for deleting an item
@login_required
def delete(request,pk):
    # Get the item by its primary key (pk) and the user who created it
    item = get_object_or_404(Item, pk=pk,created_by=request.user)
    item.delete()  # Delete the item
    return redirect('dashboard:index')  # Redirect to dashboard after deletion
