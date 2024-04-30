# import required modules and models
from .forms import fpForm
from django.shortcuts import render, redirect
from .models import clientdetails, person, requirements, user_report, logindetails, forgot_password
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http.response import HttpResponse, JsonResponse
import json
import os
import mysql.connector
import matplotlib.pyplot as plt
import numpy as np
from django.contrib import messages

# login view to authenticate users
def login(request):
    # render login page if GET request
    if request.method == 'GET':
        return render(request,'login.html')
    else: # login authentication if POST request
        # get username and password from request
        global username
        username=request.POST.get('username')
        password=request.POST.get('password')
        # filter records from login details model using username and password
        uname=logindetails.objects.filter(username=username)
        pwd=logindetails.objects.filter(password=password)

        if uname and pwd: # if username and password matches
            # get user role from login details
            dsig = logindetails.objects.filter(username=username)
            for i in dsig:
                dsg=i.role 
                # redirect to appropriate page based on user role
                if dsg =='superadmin':
                    return render(request,'SAdmin_Homepage.html') 
                elif dsg =='user':
                    return redirect(userhomepage)
                else:
                    # get user reports from user_report model
                    x=user_report.objects.filter(clientname=username)
                    y=user_report.objects.filter(clientname=username)
                    campaigns=user_report.objects.all()   
                    context={'x':x,'y':y,'campaigns':campaigns}
                    return render(request,'campaign.html',context)
        else: # if username or password is incorrect
            messages.success(request,'Invalid details!')
            return render(request,'login.html')

# view to display campaign details
def campaign_details(request):
    if request.method == 'POST':
        # get selected campaign name from POST request
        selected_campaign = request.POST.get('campaign_name')
        # filter records from user_report model using selected campaign
        campaign = user_report.objects.filter(campaign_name=selected_campaign)
        campaigns=user_report.objects.all()
        context = {'campaign': campaign,'campaigns':campaigns}
        return render(request, 'campaign.html', context)
    else:
        # get all campaigns from user_report model
        campaigns=user_report.objects.all()
        return render(request, 'campaign.html',{'campaigns':campaigns})

# view to display super admin homepage
def homepage(request):
    return render(request,'SAdmin_homepage.html')

# view to display user homepage
def userhomepage(request):
    return render(request,'User_Homepage.html')

'''
def clientform(request):
    if request.method=="POST":
        prod=clientdetails()
        prod.clientname=request.POST.get('clientname')
        
        prod.userid=request.POST.get('userid')
        prod.password=request.POST.get('password')
        prod.date=request.POST.get('date')
        prod.image=request.POST.get('image')
        #form=clientform(data=request.POST,files=request.FILES)
        
        
        prod.save()
        
    return render(request,'index2.html')
'''
# Define a function to upload images for clients
def upload_image(request):
    # If the request method is GET, display the client details that are already saved
    if request.method=='GET':
        dat=clientdetails.objects.all().values()
        return render(request,'SAdmin_ClientDetails.html',{'dat':dat}) 
        
    # If the request method is POST, process the form data and save the image for the client
    elif request.method=='POST':
        clientname=request.POST['clientname']
        # Check if the client name is already registered
        if clientdetails.objects.filter(clientname=clientname).exists():
            messages.error(request,"Client Name already registered !")  
            return render(request,'SAdmin_ClientDetails.html')

        else:
            data = dict()
            if "GET" == request.method:
                return render(request, 'SAdmin_ClientDetails.html', data)
            # Retrieve the files (images) from the POST request
            files=request.FILES
            clientname=request.POST.get('clientname')
            userid=request.POST.get('userid')
            password=request.POST.get('password')
            date=request.POST.get('date')
            image = files.get("image")
            # Create a new instance of the clientdetails model and save the form data
            instance = clientdetails()
            instance.clientname = clientname
            instance.userid = userid
            instance.password = password
            instance.date = date
            instance.image = image
            instance.save()
            # Display a success message and render the template for uploading client images
            messages.success(request,"Form Submitted Successfully")
            return render(request, 'SAdmin_ClientDetails.html')

# Define a function to view campaign requirements data
def taskdata(request):
    # Retrieve all the requirements from the model and render the template to display the data
    td=requirements.objects.all()
    return render(request,'SAdmin_Taskdata.html',{'td':td})

# Define a function to create a campaign
def taskcreation(request):
    # If the request method is GET, display the template to create a new campaign and provide a list of clients to choose from
    if request.method=='GET':
        people = clientdetails.objects.all()
        return render(request,'taskcreation.html',{'people': people})
    
    # If the request method is POST, process the form data and save the new campaign
    elif request.method=='POST':
        people=requirements.objects.all().values()
        campaign_name=request.POST['campaign_name']
        # Check if the campaign name is already registered
        if requirements.objects.filter(campaign_name=campaign_name).exists():
            messages.error(request,"Campaign Name already registered !")  
            return render(request,'taskcreation.html',{'people': people})
        
        else:
            # Create a new instance of the requirements model and save the form data
            requirements(
                name=request.POST.get('name'),
                campaign_name=request.POST.get('campaign_name'),
                start_date=request.POST.get('start_date'),
                end_date=request.POST.get('end_date'),
                planned_impressions=request.POST.get('planned_impressions'),
                planned_cpm=request.POST.get('planned_cpm'),
                planned_cpc=request.POST.get('planned_cpc'),
                planned_cost=request.POST.get('planned_cost'),
                deptid_id=request.POST.get('deptid_id')
            ).save()
            # Display a success message, provide a list of clients to choose from, and render the template to create a new campaign
            messages.success(request,"Form Submitted Successfully")
            people = clientdetails.objects.all()
            return render(request,'taskcreation.html',{'people': people})



# This function deletes campaign requirements data based on the provided ID
def delete(request, id):
    # Get the requirements object with the provided ID
    td = requirements.objects.get(id=id)
    # Delete the object
    td.delete()
    # Redirect the user to the taskdata page
    return redirect("/taskdata")

# This function retrieves the campaign requirements data based on the provided ID for editing
def edit(request, id):
    # Get the requirements object with the provided ID
    td = requirements.objects.get(id=id)
    # Render the edittaskdata.html template with the requirements object as a context variable
    return render(request,'edittaskdata.html',{'td':td})

# This function updates the campaign requirements data based on the provided ID
def update(request, id):
    # Retrieve the updated data from the POST request
    campaign_name=request.POST.get('campaign_name')
    start_date=request.POST.get('start_date')
    end_date=request.POST.get('end_date')
    planned_impressions=request.POST.get('planned_impressions')
    planned_cpm=request.POST.get('planned_cpm')
    planned_cpc=request.POST.get('planned_cpc')
    planned_cost=request.POST.get('planned_cost')
    deptid_id = request.POST.get('deptid_id')
    
    # Get the requirements object with the provided ID
    td = requirements.objects.get(id=id)

    # Update the requirements object with the new data
    td.campaign_name=campaign_name
    td.start_date=start_date
    td.end_date=end_date
    td.planned_impressions=planned_impressions
    td.planned_cpm=planned_cpm
    td.planned_cpc=planned_cpc
    td.planned_cost=planned_cost
    td.deptid_id=deptid_id

    # Save the updated object
    td.save()

    # Redirect the user to the taskdata page
    return redirect(taskdata)
    return render({'people': people})  
    # return render(request, 'template_name.html', {'context_variable_name': context_variable_value})

    
    
          
'''
def u_report(request):
    if request.method=='GET':
        people = clientdetails.objects.all()
        rd=user_report.objects.all()
        return render(request,'user_report.html',{'people': people},{'rd':rd})
    else:
        user_report(
            name=request.POST.get('name'),
            campaign_name=request.POST.get('campaign_name'),
            date=request.POST.get('date'),
            no_of_impressions=request.POST.get('no_of_impressions'),
            no_of_clicks=request.POST.get('no_of_clicks'),
            cost_per_impressions=request.POST.get('cost_per_impressions'),
            cost_per_click=request.POST.get('cost_per_click'),
            total_cost_per_impressions=request.POST.get('total_cost_per_impressions'),
            total_cost_per_click=request.POST.get('total_cost_per_click'),
            cost_per_day=request.POST.get('cost_per_day')

        ).save()
        people = clientdetails.objects.all()
        return render(request,'user_report.html',{'people': people})
'''



# View to display report data and search for reports by date range
def reportdata(request):
    if request.method == "POST":
        # If the request method is POST, retrieve the date range from the form
        datef = request.POST.get("datef")
        datet = request.POST.get("datet")
        # Filter the user_report objects based on the date range
        queryset = user_report.objects.filter(date__range=[datef, datet])
        # Return the search results to a template
        return render(request, 'searchresult.html', {'queryset': queryset})
    else:
        # If the request method is not POST, retrieve all user_report objects
        rd = user_report.objects.all()
        # Return the report data to a template
        return render(request, 'SAdmin_Reportdata.html', {'rd': rd})

# View to delete a report entry
def delete_report(request, id):
    # Retrieve the user_report object with the specified id
    rd = user_report.objects.get(id=id)
    # Delete the user_report object
    rd.delete()
    # Redirect to the reportdata view
    return redirect("/reportdata")

# View to display a form to edit a report entry
def edit_report(request, id):    
    # Retrieve the user_report object with the specified id
    rd = user_report.objects.get(id=id)
    # Return the user_report object to a template
    return render(request, 'editreportdata.html', {'rd': rd})

# View to update a report entry
def update_report(request, id):
    # Retrieve the user_report object with the specified id
    rd = user_report.objects.get(id=id)
    # Retrieve the updated data from the form
    date = request.POST.get('date')
    no_of_impressions = request.POST.get('no_of_impressions')
    no_of_clicks = request.POST.get('no_of_clicks')
    cost_per_impressions = request.POST.get('cost_per_impressions')
    cost_per_click = request.POST.get('cost_per_click')
    total_cost_per_impressions = request.POST.get('total_cost_per_impressions')
    total_cost_per_click = request.POST.get('total_cost_per_click')
    cost_per_day = request.POST.get('cost_per_day')

    # Update the user_report object with the new data
    rd.date = date
    rd.no_of_impressions = no_of_impressions
    rd.no_of_clicks = no_of_clicks
    rd.cost_per_impressions = cost_per_impressions
    rd.cost_per_click = cost_per_click
    rd.total_cost_per_impressions = total_cost_per_impressions
    rd.total_cost_per_click = total_cost_per_click
    rd.cost_per_day = cost_per_day

    # Save the updated user_report object
    rd.save()
    # Redirect to the reportdata view
    return redirect(reportdata)

# View to display client details
def viewclientdetails(request):
    # Retrieve all clientdetails objects
    people = clientdetails.objects.all()
    # Return the client details to a template
    return render(request, 'SAdmin_ViewClientDetails.html', {'people': people})

# View to delete a client entry
def delete_client(request, id):
    # Retrieve the clientdetails object with the specified id
    people = clientdetails.objects.get(id=id)
    # Delete the clientdetails object
    people.delete()
    # Redirect to the viewclientdetails view
    return redirect("/viewclientdetails")

'''
def edit_client(request, id):

    people=clientdetails.objects.get(id=id)
    return render(request,'editclientdata.html',{'people':people})
'''
# Import necessary modules
import os

# Function to display client details for editing
def edit_client1(request, id):
    # Retrieve client details based on ID
    people=clientdetails.objects.get(id=id)
    # Render edit3.html template with client details
    return render(request,'edit3.html',{'people':people})

# Function to update client details
def update_client(request, id):
    # Retrieve client details based on ID
    people=clientdetails.objects.get(id=id)
    # If HTTP request method is POST
    if request.method == "POST":
        # If a file is uploaded
        if len(request.FILES) != 0:
            # If client already has an image, remove it from storage
            if len(people.image) > 0:
                os.remove(people.image.path)
            # Set client image to the uploaded file
            people.image = request.FILES['image']
        # Update client name, user ID, password and date
        people.clientname = request.POST.get('clientname')
        people.userid = request.POST.get('userid')
        people.password = request.POST.get('password')
        people.date=request.POST.get('date')
        # Save the updated client details
        people.save()
        # Redirect to viewclientdetails page
        return redirect(viewclientdetails)
    # If HTTP request method is not POST
    else:
        # Render SAdmin_ViewClientDetails.html template with client details
        context = {'people':people}
        return render(request, 'SAdmin_ViewClientDetails.html', context)

'''
# Function for user login
def newlogin(request):
    # If HTTP request method is GET, render login.html template
    if request.method == 'GET':
        return render(request,'login.html')
    # If HTTP request method is POST
    else:
        # Retrieve username and password from HTTP POST request
        global username
        username=request.POST.get('username')
        password=request.POST.get('password')
        # Query the logindetails model to check if the provided username and password match
        uname=logindetails.objects.filter(username=username)
        pwd=logindetails.objects.filter(password=password)
        # If the provided username and password match
        if uname and pwd:
            # Query the logindetails model to retrieve the role of the user
            dsig = logindetails.objects.filter(username=username)
            for i in dsig:
                dsg=i.role 
                # If user is a superadmin, render SAdmin_Homepage.html template
                if dsg =='superadmin':
                    return render(request,'SAdmin_Homepage.html') 
                # If user is not a superadmin, redirect to userhomepage page
                else:
                    return redirect(userhomepage)
        # If the provided username and password do not match
        else:
            # Render login.html template
            return render(request,'login.html')

'''

# Function for forgot password feature
def forgotpassword(request):
    # If HTTP request method is POST
    if request.method == 'POST':
        # Create an instance of fpForm model with the form data
        form1 = fpForm(request.POST)
        # If the form data is valid
        if form1.is_valid():
            # Create an instance of the forgot_password model with the password and confirm_password fields
            table2_instance = forgot_password(password=form1.cleaned_data['password'], confirm_password=form1.cleaned_data['confirm_password'])
            # Save the instance of the forgot_password model
            table2_instance.save()
            # Retrieve email and password from HTTP POST request
            mail=request.POST.get('mail')
            password=request.POST.get('password')
            # Query the log

            # Check if there is a user with the given email in the logindetails table
    p = logindetails.objects.filter(mail=mail)
    
    # If there is a user with the given email, update their password and show a success message
    if p:
        p.update(password=password)
        e = "Password Changed Successfully"
        
        # Redirect to the forgot password page with the success message
        return render(request, 'forgotpassword.html',{'e':e})
    
# If the request method is not POST, then show the forgot password form
    else:
        form1 = fpForm()

# Render the forgot password page with the form or the success message if it exists
        return render(request, 'forgotpassword.html', {'form1': form1})



# Define a function called "u_report" that takes a request object as input
def u_report(request):
    # If the request method is GET
    if request.method=='GET':
        # Get all the records from the clientdetails model and store it in "people" variable
        people = clientdetails.objects.all()
        # Get all the records from the requirements model and store it in "empcontext" variable
        empcontext = requirements.objects.all()    
        # Create a dictionary called "context" with "people" and "empcontext" variables as its values
        context={'people':people,'empcontext':empcontext}
        # Render the "user_report.html" template with the "context" dictionary
        return render(request,'user_report.html',context)
    
    # If the request method is POST
    elif request.method=='POST':
        # Get the "date" value from the POST request
        date=request.POST['date']
        # If there is already a record in the user_report model with the same date value
        if user_report.objects.filter(date=date).exists():
            # Get all the records from the requirements model and store it in "empcontext" variable
            empcontext = requirements.objects.all()    
            # Create a dictionary called "context" with "empcontext" variable as its value
            context={'empcontext':empcontext}
            # Display an error message using Django messages framework
            messages.error(request,"Given Date Already Registered !")  
            # Render the "user_report.html" template with the "context" dictionary
            return render(request,'user_report.html',context)

        # If there is no record in the user_report model with the same date value
        else:
            # Create a new record in the user_report model with the values received from the POST request
            user_report(
                clientname=request.POST.get('hiddenclient'),
                campaign_name=request.POST.get('hiddencampaign'),
                date=request.POST.get('date'),
                no_of_impressions=request.POST.get('no_of_impressions'),
                no_of_clicks=request.POST.get('no_of_clicks'),
                cost_per_impressions=request.POST.get('cost_per_impressions'),
                cost_per_click=request.POST.get('cost_per_click'),
                total_cost_per_impressions=request.POST.get('total_cost_per_impressions'),
                total_cost_per_click=request.POST.get('total_cost_per_click'),
                cost_per_day=request.POST.get('cost_per_day')
            ).save()
            # Get all the records from the clientdetails model and store it in "people" variable
            people = clientdetails.objects.all()
            # Get all the records from the requirements model and store it in "empcontext" variable
            empcontext = requirements.objects.all()    
            # Create a dictionary called "context" with "people" and "empcontext" variables as its values
            context={'people':people,'empcontext':empcontext}
            # Display a success message using Django messages framework
            messages.success(request,'Form Submitted Successfully')
            # Render the "user_report.html" template with the "context" dictionary
            return render(request,'user_report.html',context)


# Define a view function to report user activity
def report_user(request):
    # Check if the request method is GET
    if request.method=='GET':
        # Retrieve all the client details from the clientdetails model
        people = clientdetails.objects.all()
        # Retrieve all the requirements from the requirements model
        empcontext = requirements.objects.all()    
        # Create a dictionary of the retrieved data and send it to the user_report_user.html template
        context={'people':people,'empcontext':empcontext}
        return render(request,'user_report_user.html',context)
    
    # Check if the request method is POST
    elif request.method=='POST':
        # Retrieve the date submitted by the user
        date=request.POST['date']
        # Check if the date already exists in the user_report model
        if user_report.objects.filter(date=date).exists():
            # Retrieve all the requirements from the requirements model
            empcontext = requirements.objects.all()    
            context={'empcontext':empcontext}
            # Display an error message if the date already exists
            messages.error(request,"Given Date Already Registered !")  
            return render(request,'user_report_user.html',context)
        
        else:
            # Save the user's report data to the user_report model
            user_report(
                clientname=request.POST.get('hiddenclient'),
                campaign_name=request.POST.get('hiddencampaign'),
                date=request.POST.get('date'),
                no_of_impressions=request.POST.get('no_of_impressions'),
                no_of_clicks=request.POST.get('no_of_clicks'),
                cost_per_impressions=request.POST.get('cost_per_impressions'),
                cost_per_click=request.POST.get('cost_per_click'),
                total_cost_per_impressions=request.POST.get('total_cost_per_impressions'),
                total_cost_per_click=request.POST.get('total_cost_per_click'),
                cost_per_day=request.POST.get('cost_per_day')
            ).save()
            # Retrieve all the client details from the clientdetails model
            people = clientdetails.objects.all()
            # Retrieve all the requirements from the requirements model
            empcontext = requirements.objects.all()    
            # Create a dictionary of the retrieved data and send it to the user_report_user.html template
            context={'people':people,'empcontext':empcontext}
            # Display a success message if the data is successfully saved
            messages.success(request,'Form Submitted Successfully')
            return render(request,'user_report_user.html',context)



# Defining a function to generate a pie chart
def piechart(request):
    # Connecting to the MySQL database
    mydb= mysql.connector.connect(user='root',password='admin',database='quality')
    mycursor = mydb.cursor()
    
    # Retrieving data from the database
    mycursor.execute('select no_of_impressions, no_of_clicks from q_app_user_report')
    result=mycursor.fetchall()
    print(result)
    
    # Creating empty lists to store values of no_of_impressions and no_of_clicks
    no_of_impressions=[]
    no_of_clicks=[]
    
    # Appending values of no_of_impressions and no_of_clicks from the retrieved data
    for i in result:
        no_of_impressions.append(i[0])
        no_of_clicks.append(i[1])
        
    # Converting no_of_clicks list to a NumPy array
    y=np.array([no_of_clicks])
    
    # Generating a pie chart using Matplotlib
    plt.pie(no_of_clicks,labels=no_of_impressions)
    plt.title('pie chart',color='orange')
    plt.xlabel('',color='GREEN')
    plt.show()
    
    # Rendering the piechart.html template
    return render(request,'piechart.html')



# Define a function named "client1" that accepts a request object
def client1(request):
    # Check if the request method is POST
    if request.method=="POST":
        # Get the "datef" and "datet" values from the POST data
        datef=request.POST.get("datef")
        datet=request.POST.get("datet")
        # Filter user_report objects by date range using "datef" and "datet"
        q = user_report.objects.filter(date__range=[datef, datet])
        # Get all clientdetails objects
        people = clientdetails.objects.all()
        # Create a context dictionary with "people" and "q" keys
        context={'people':people,'q':q}
        # Render the clientresult.html template with the context data
        return render(request,'clientresult.html',context)
    else:
        # Get all user_report objects
        customer=user_report.objects.all()
        # Get all clientdetails objects
        people = clientdetails.objects.all()
        # Create a context dictionary with "people" and "customer" keys
        context={'people':people,'customer':customer}
        # Render the client1.html template with the context data
        return render(request,'client1.html',context)

    

