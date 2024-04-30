from django.db import models
import os

# Importing CASCADE from deletion module
from django.db.models.deletion import CASCADE

# Importing Model class from base module
from django.db.models.base import Model


# Create a model for storing login details
class logindetails(models.Model):
    # Defining fields for the model
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    role = models.CharField(max_length=20)
    mail = models.EmailField(max_length=30)


# Function to define upload path for client images
def upload_path(instance, filename):
    # Change the filename here if required
    return os.path.join("uploads", filename)


# Create a model for storing client details
class clientdetails(models.Model):
    # Defining fields for the model
    clientname = models.CharField(max_length=50)
    userid = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    date = models.CharField(max_length=50)
    image = models.ImageField(upload_to=upload_path) # Upload client image


# Create a model for storing client requirements
class requirements(models.Model):
    # Define a foreign key to link the clientdetails model
    deptid = models.ForeignKey(clientdetails, on_delete=CASCADE)
    # Defining fields for the model
    name = models.CharField(max_length=100)
    campaign_name = models.CharField(max_length=100)
    start_date = models.CharField(max_length=100)
    end_date = models.CharField(max_length=100)
    planned_impressions = models.CharField(max_length=100)
    planned_cpm = models.CharField(max_length=100)
    planned_cpc = models.CharField(max_length=100)
    planned_cost = models.CharField(max_length=100)

    # Defining a string representation of the model
    def __str__(self):
        return self.name


# Create a model for storing person details
class person(models.Model):
    # Defining fields for the model
    name = models.CharField(max_length=100)


# Create a model for storing user reports
class user_report(models.Model):
    # Defining fields for the model
    clientname = models.CharField(max_length=100)
    campaign_name = models.CharField(max_length=100)
    date = models.CharField(max_length=10)
    no_of_impressions = models.IntegerField()
    no_of_clicks = models.IntegerField()
    cost_per_impressions = models.IntegerField()
    cost_per_click = models.IntegerField()
    total_cost_per_impressions = models.IntegerField()
    total_cost_per_click = models.IntegerField()
    cost_per_day = models.IntegerField()


# Create a model for forgot password
class forgot_password(models.Model):
    # Defining fields for the model
    password = models.CharField(max_length=50)
    confirm_password = models.CharField(max_length=50)
