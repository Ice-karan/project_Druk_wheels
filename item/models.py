from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    # The name of the category, which must be unique and can be up to 255 characters long
    name = models.CharField(max_length=255, unique=True)
    
    class Meta:
        # Orders the categories by their name in ascending order
        ordering = ('name',)
        # Changes the plural form in the admin interface
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        # Returns the name of the category when converting the object to a string
        return self.name


class Item(models.Model):
    # Foreign key relationship to Category, if a category is deleted, its related items are also deleted
    category = models.ForeignKey(Category, related_name='cars', on_delete=models.CASCADE)
    # The brand or make of the car, with a default value
    name = models.CharField(max_length=255, default='Maruti Suzuki')
    # The location where the car is being sold, with a default value
    location = models.CharField(max_length=255, default='Thimphu')
    # The manufacturing year of the car, with a default value
    year = models.PositiveIntegerField(default=2010)
    # A text field for the description of the car, which can be blank or null
    description = models.TextField(blank=True, null=True)
    # The mileage of the car, with a default value
    mileage = models.PositiveIntegerField(default=0)
    # The color of the car, which can be blank or null
    color = models.CharField(max_length=100, blank=True, null=True)
    # The type of transmission, with a default value, which can be blank or null
    transmission = models.CharField(max_length=100, default='Unknown Transmission', blank=True, null=True)
    # The type of fuel, with a default value, which can be blank or null
    fuel_type = models.CharField(max_length=100, default='Unknown Fuel Type', blank=True, null=True)
    # The price of the car, with a default value
    price = models.FloatField(default=0.0)
    # An image of the car, uploaded to 'car_images', which can be blank or null
    image = models.ImageField(upload_to='car_images', blank=True, null=True)
    # A boolean field indicating whether the car is sold, with a default value
    is_sold = models.BooleanField(default=False)
    # A foreign key relationship to the User who created the item, if the user is deleted, their items are also deleted
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cars')
    # The date and time when the item was created, automatically set when the item is created
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        # Returns a string representation of the item, including its make, model, and year
        return f'{self.name} '
