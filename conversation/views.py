from django.shortcuts import render, get_object_or_404, redirect
from item.models import Item  # Import the Item model from the item app
from .forms import ConversationMessageForm  # Import the ConversationMessageForm from the current app
from .models import Conversation  # Import the Conversation model from the current app
from django.contrib.auth.decorators import login_required  # Import the login_required decorator
from django_ratelimit.decorators import ratelimit  # Import rate limiting decorator

# The following views require the user to be logged in (`@login_required`)

@login_required
@ratelimit(key='user', rate='10/m', method='POST', block=True)
def new_conversation(request, item_pk):
    """
    Initiates a new conversation about an item.

    Args:
        request: The HTTP request object.
        item_pk: The primary key of the item the conversation is about.

    Returns:
        A redirect response to either the dashboard or conversation detail page.
    """

    item = get_object_or_404(Item, pk=item_pk)  # Get the item object

    # Prevent the item creator from starting a conversation with themselves
    if item.created_by == request.user:
        return redirect('dashboard:index')

    # Check if the user is already part of an existing conversation for this item
    conversations = Conversation.objects.filter(item=item).filter(members__in=[request.user.id])

    if conversations:
        return redirect('conversation:detail', pk=conversations.first().id)

    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)  # Create a form instance with POST data

        if form.is_valid():
            # Create a new conversation
            conversation = Conversation.objects.create(item=item)
            # Add the current user and item creator as participants
            conversation.members.add(request.user)
            conversation.members.add(item.created_by)
            conversation.save()

            conversation_message = form.save(commit=False)  # Create a conversation message instance
            conversation_message.conversation = conversation  # Set the conversation for the message
            conversation_message.created_by = request.user  # Set the message creator
            conversation_message.save()

            return redirect('item:detail', pk=item_pk)  # Redirect to item detail page after successful creation

    else:
        form = ConversationMessageForm()  # Create an empty form instance

    return render(request, 'conversation/new.html', {
        'form': form,  # Pass the form to the template
    })


@login_required
def inbox(request):
    """
    Displays a list of all conversations the user is involved in.

    Args:
        request: The HTTP request object.

    Returns:
        A rendered response with the list of conversations.
    """

    conversations = Conversation.objects.filter(members__in=[request.user.id])  # Get user's conversations

    return render(request, 'conversation/inbox.html', {
        'conversations': conversations,  # Pass conversations to the template
    })


@login_required
@ratelimit(key='user', rate='20/m', method='POST', block=True)
def detail(request, pk):
    """
    Displays the details of a specific conversation and allows sending new messages.

    Args:
        request: The HTTP request object.
        pk: The primary key of the conversation to view.

    Returns:
        A rendered response with conversation details and a message form.
    """

    conversation = Conversation.objects.filter(members__in=[request.user.id]).get(pk=pk)  # Get conversation

    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)  # Create a form instance with POST data

        if form.is_valid():
            conversation_message = form.save(commit=False)  # Create a conversation message instance
            conversation_message.conversation = conversation  # Set the conversation for the message
            conversation_message.created_by = request.user  # Set the message creator
            conversation_message.save()

            return redirect('conversation:detail', pk=pk)  # Redirect back to conversation detail

    else:
        form = ConversationMessageForm()  # Create an empty form instance

    return render(request, 'conversation/detail.html', {
        'conversation': conversation,  # Pass conversation details to the template
        'form': form,  # Pass the form to the template
    })