from django.db import models
from item.models import Item  # Importing the Item model
from django.contrib.auth.models import User  # Importing the User model
from .utils import encrypt_message, decrypt_message  # Import encryption utilities

class Conversation(models.Model):
    # A conversation belongs to an item and can have multiple members (users)
    item = models.ForeignKey(Item, related_name='conversations', on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name='conversations')  # Many-to-many relationship with User model
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the conversation was created
    modified_at = models.DateTimeField(auto_now=True)     # Timestamp for the last modification

    class Meta:
        ordering = ('-modified_at',)  # Ordering conversations by modification time, newest first

    def __str__(self):
        return self.item.name  # String representation of the conversation (the name of the item)

class ConversationMessage(models.Model):
    # A message belongs to a conversation and is created by a user
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()  # Encrypted content of the message
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the message was created
    created_by = models.ForeignKey(User, related_name='created_messages', on_delete=models.CASCADE)  # Message creator

    def save(self, *args, **kwargs):
        if not self.pk:  # Encrypt only on creation
            self.content = encrypt_message(self.content)
        super().save(*args, **kwargs)

    @property
    def decrypted_content(self):
        return decrypt_message(self.content)

    def __str__(self):
        return self.decrypted_content  # String representation of the decrypted message
