from django.shortcuts import render,redirect
from .models import clientdetails,person,requirements,user_report,logindetails
from django.db.models import Q
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render,redirect
from django.contrib import messages
#from .models import requirements,clientdata,user_report
from django.core import serializers
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
import json
import os
import mysql.connector
import matplotlib.pyplot as plt
import numpy as np

import os
import mysql.connector
import matplotlib.pyplot as plt
import numpy as np
import mysql.connector
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import base64


# Create your views here.

def login(request):
    if request.method == 'GET':
        return render(request,'login.html')
    else: #login authentication
        global username
        username=request.POST.get('username')
        password=request.POST.get('password')
        uname=logindetails.objects.filter(username=username)
        pwd=logindetails.objects.filter(password=password)

        if uname and pwd:
            dsig = logindetails.objects.filter(username=username)
            for i in dsig:
                dsg=i.role 
                if dsg =='superadmin':
                    return render(request,'SAdmin_Homepage.html') 
                elif dsg =='user':
                    return redirect(userhomepage)
                elif dsg=='client2':
                    return redirect(client2)
                elif dsg=='client3':
                    return redirect(client3)
                
                else:
                    return redirect(clientpage)

                
                
        else:
            messages.success(request,'Invalid details!')
            return render(request,'login.html')
'''
def loginpage(request):
    if request.method=='GET':
        return render(request,'loginpage.html')
    else:
        username = request.POST['username']
        password = request.POST['password']
        if username=='superadmin@123' and password=='super':
            return render(request,'SAdmin_Homepage.html')
        elif username=='user@123' and password=='user123':
            return render(request,'User_Homepage.html')
        elif username=='client1@123' and password=='client1@123':
            report = user_report.objects.all()
            return render(request,'client1.html',{'report':report})
        else:
            return render(request,'loginpage.html')
'''

def homepage(request):
    
    return render(request,'SAdmin_homepage.html')

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

def upload_image(request):
    if request.method=='GET':
        dat=clientdetails.objects.all().values()  #displaying the values that are before saved
         
        return render(request,'SAdmin_ClientDetails.html',{'dat':dat}) 
          
    
    # elif request.method=='POST':
    #      clientname=request.POST['clientname']
    #      if clientdetails.objects.filter(clientname=clientname).exists(): # it checks client name is already registered or not
    #         messages.error(request,"Client Name already registered !")  
    #      return render(request,'SAdmin_ClientDetails.html')

    else:
        data = dict()
        if "GET" == request.method:
            return render(request, 'SAdmin_ClientDetails.html', data)
        # process POST request
        files = request.FILES  # multivalued dict
        clientname=request.POST.get('clientname')
    
        userid=request.POST.get('userid')
        password=request.POST.get('password')
        date=request.POST.get('date')
        image = files.get("image")
        instance = clientdetails()
        instance.clientname = clientname
    
        instance.userid = userid
        instance.password = password
        instance.date = date
        instance.image = image
        instance.save()
        #p=ImageModel.objects.all()
        return render(request, 'SAdmin_ClientDetails.html')

def taskdata(request):
    td=requirements.objects.all()
    return render(request,'SAdmin_Taskdata.html',{'td':td})

def taskcreation(request):
    
    if request.method=='GET':
        people = clientdetails.objects.all()
        return render(request,'taskcreation.html',{'people': people})
    else:
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
       # messages.success(request,'Form Submitted Successfully')
        people = clientdetails.objects.all()
        return render(request,'taskcreation.html',{'people': people})

def delete(request, id):
    td=requirements.objects.get(id=id)
    td.delete()
    return redirect("/taskdata")

def edit(request, id):

    td=requirements.objects.get(id=id)
    return render(request,'edittaskdata.html',{'td':td})

def update(request, id):
 
    #people = Person.objects.get(id=id)
    #name=request.POST.get('name'),
    campaign_name=request.POST.get('campaign_name')
    start_date=request.POST.get('start_date')
    end_date=request.POST.get('end_date')
    planned_impressions=request.POST.get('planned_impressions')
    planned_cpm=request.POST.get('planned_cpm')
    planned_cpc=request.POST.get('planned_cpc')
    planned_cost=request.POST.get('planned_cost')

    td=requirements.objects.get(id=id)

    #td.name=name
    


    td.campaign_name=campaign_name
    td.start_date=start_date
    td.end_date=end_date
    td.planned_impressions=planned_impressions
    td.planned_cpm=planned_cpm
    td.planned_cpc=planned_cpc
    td.planned_cost=planned_cost

    td.save()
    
    return redirect(taskdata) 
    return render({'people': people})       
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



def reportdata(request):
    if request.method=="POST":
        datef=request.POST.get("datef")
        datet=request.POST.get("datet")
        queryset = user_report.objects.filter(date__range=[datef, datet])
        #rd=user_report.objects.all()
        return render(request,'searchresult.html',{'queryset':queryset})
    else:
        rd=user_report.objects.all()
        return render(request,'SAdmin_Reportdata.html',{'rd':rd})



def delete_report(request, id):
    rd=user_report.objects.get(id=id)
    rd.delete()
    return redirect("/reportdata")

def edit_report(request, id):    
    rd=user_report.objects.get(id=id)
    return render(request,'editreportdata.html',{'rd':rd})

def update_report(request, id):
    
    #people = Person.objects.get(id=id)
    #name=request.POST.get('name'),
    date=request.POST.get('date')
    no_of_impressions=request.POST.get('no_of_impressions')
    no_of_clicks=request.POST.get('no_of_clicks')
    cost_per_impressions=request.POST.get('cost_per_impressions')
    cost_per_click=request.POST.get('cost_per_click')
    total_cost_per_impressions=request.POST.get('total_cost_per_impressions')
    total_cost_per_click=request.POST.get('total_cost_per_click')
    cost_per_day=request.POST.get('cost_per_day')
    rd=user_report.objects.get(id=id)

    #td.name=name
    rd.date=date
    rd.no_of_impressions=no_of_impressions
    rd.no_of_clicks=no_of_clicks
    rd.cost_per_impressions=cost_per_impressions
    rd.cost_per_click=cost_per_click
    rd.total_cost_per_impressions=total_cost_per_impressions
    rd.total_cost_per_click=total_cost_per_click
    rd.cost_per_day=cost_per_day

    rd.save()
    return redirect(reportdata) 
    return render({'people': people})




def viewclientdetails(request):
    people=clientdetails.objects.all()
    #image=clientdetails.objects
    return render(request,'SAdmin_ViewClientDetails.html',{'people':people})


def delete_client(request, id):
    people=clientdetails.objects.get(id=id)
    people.delete()
    return redirect("/viewclientdetails")
'''
def edit_client(request, id):

    people=clientdetails.objects.get(id=id)
    return render(request,'editclientdata.html',{'people':people})
'''
def edit_client1(request, id):

    people=clientdetails.objects.get(id=id)
    return render(request,'edit3.html',{'people':people})

import os
def update_client(request, id):
    
    people=clientdetails.objects.get(id=id)
    if request.method == "POST":
        if len(request.FILES) != 0:
            if len(people.image) > 0:
                os.remove(people.image.path)
            people.image = request.FILES['image']
        people.clientname = request.POST.get('clientname')
        people.userid = request.POST.get('userid')
        people.password = request.POST.get('password')
        people.date=request.POST.get('date')
        people.save()
        #messages.success(request, "Product Updated Successfully")
        return redirect(viewclientdetails)    

    context = {'people':people}
    return render(request, 'SAdmin_ViewClientDetails.html', context)

'''
def newlogin(request):
    if request.method == 'GET':
        return render(request,'login.html')
    else: #login authentication
        global username
        username=request.POST.get('username')
        password=request.POST.get('password')
        uname=logindetails.objects.filter(username=username)
        pwd=logindetails.objects.filter(password=password)

        if uname and pwd:
            dsig = logindetails.objects.filter(username=username)
            for i in dsig:
                dsg=i.role 
                if dsg =='superadmin':
                    return render(request,'SAdmin_Homepage.html') 
                else:
                    return redirect(userhomepage)

                
                
        else:
            #messages.success(request,'Invalid details!')
            return render(request,'login.html')

'''
def forgotpassword(request):
    if request.method=="GET":

        #ld=logind.objects.all()
        return render(request,'forgotpassword.html')
    else:
        
        mail=request.POST.get('mail')
        password=request.POST.get('password')
        p=logindetails.objects.filter(mail=mail)
        if p:
            p.update(password=password)
            e="Password Changed Successfully"
            return render(request,'forgotpassword.html',{'e':e})
        
def u_report(request):
    if request.method=='GET':
        people = clientdetails.objects.all()
        #deptcontext = clientdetails.objects.all()
        empcontext = requirements.objects.all()    
        context={'people':people,'empcontext':empcontext}
        return render(request,'user_report.html',context)
    else:
        user_report(
            clientname=request.POST.get('clientname'),
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
        #deptcontext = clientdetails.objects.all()
        empcontext = requirements.objects.all()    
        context={'people':people,'empcontext':empcontext}
        return render(request,'user_report.html',context)



def piechart(request):
    mydb= mysql.connector.connect(user='root',password='admin',database='quality')
    mycursor = mydb.cursor()
    mycursor.execute('select no_of_impressions, no_of_clicks from q_app_user_report')
    result=mycursor.fetchall()
    print(result)
    no_of_impressions=[]
    no_of_clicks=[]
    for i in result:
        no_of_impressions.append(i[0])
        no_of_clicks.append(i[1])
    y=np.array([no_of_clicks])
    # def absolute_value(val):
    #     a=np.round(val/100.*y.sum(),0)
    #     return a
    plt.pie(no_of_clicks,labels=no_of_impressions)
    plt.title('pie chart',color='orange')
    plt.xlabel('',color='GREEN')
    plt.show()
    return render(request,'piechart.html')






def clientpage(request):
    q=user_report.objects.filter(clientname='2')
    people=clientdetails.objects.filter(clientname='wipro')
    context={'q':q,'people':people}
    return render(request,'clientpage.html',context)
    

def client2(request):
    q=user_report.objects.filter(clientname='3')
    people=clientdetails.objects.filter(clientname='infosys')
    context={'q':q,'people':people}
    return render(request,'client2.html',context)


def client3(request):
    q=user_report.objects.filter(clientname='4')
    people=clientdetails.objects.filter(clientname='tesla')
    context={'q':q,'people':people}
    return render(request,'client3.html',context)


def taskcreation_user(request):
    
    if request.method=='GET':
        people = clientdetails.objects.all()
        return render(request,'taskcreation_user.html',{'people': people})
    else:
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
        people = clientdetails.objects.all()
        return render(request,'taskcreation_user.html',{'people': people})
    

def u_report_user(request):
    if request.method=='GET':
        people = clientdetails.objects.all()
        #deptcontext = clientdetails.objects.all()
        empcontext = requirements.objects.all()    
        context={'people':people,'empcontext':empcontext}
        return render(request,'user_report_user.html',context)
    else:
        user_report(
            clientname=request.POST.get('clientname'),
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
        #deptcontext = clientdetails.objects.all()
        empcontext = requirements.objects.all()    
        context={'people':people,'empcontext':empcontext}
        messages.success(request,'Form Submitted Successfully')
        return render(request,'user_report_user.html',context)



# impressions
def impressions(request):
    # Connect to the database
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="ramya",
        database="final"
    )
    # Fetch the data
    cursor = conn.cursor()
    cursor.execute("SELECT date,no_of_impressions FROM q_app_user_report")
    data = cursor.fetchall()
    # Create a Matplotlib figure
    fig, ax = plt.subplots()
    ax.plot([row[0] for row in data], [row[1] for row in data])
    ax.set_xlabel('DATES')
    ax.set_ylabel('NO OF IMPRESSIONS')
    ax.set_title('Graph')
   
    # Save the figure to a temporary file
    tmpfile = BytesIO()
    fig.savefig(tmpfile, format='png')
    plt.close(fig)

    # Read the temporary file and convert it to a base64-encoded string
    img_data = tmpfile.getvalue()
    encoded_img_data = base64.b64encode(img_data).decode('utf-8')

    # Pass the encoded image data to the template
    return render(request, 'graph.html', {'img_data': encoded_img_data})


# clicks
def clicks(request):
    # Connect to the database
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Dibya@123",
        database="final"
    )

    # Fetch the data
    cursor = conn.cursor()
    cursor.execute("SELECT date,no_of_clicks FROM q_app_user_report")
    data = cursor.fetchall()

    # Create a Matplotlib figure
    fig, ax = plt.subplots()
    ax.plot([row[0] for row in data], [row[1] for row in data])
    ax.set_xlabel('DATES')
    ax.set_ylabel('clicks')
    ax.set_title('Graph')
   
    # Save the figure to a temporary file
    tmpfile = BytesIO()
    fig.savefig(tmpfile, format='png')
    plt.close(fig)

    # Read the temporary file and convert it to a base64-encoded string
    img_data = tmpfile.getvalue()
    encoded_img_data = base64.b64encode(img_data).decode('utf-8')

    # Pass the encoded image data to the template
    return render(request, 'clicksgraph.html', {'img_data': encoded_img_data})




# clicks chart
def clickschart(request):
    sales_data = user_report.objects.all()
    categories = [sale.date for sale in sales_data]
    amounts = [float(sale.no_of_clicks) for sale in sales_data]
    plt.pie(amounts, labels=categories)
    plt.xlabel('clicks')
    plt.title('NO OF CLICKS IN A DAY')
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')
    return render(request, 'chart.html', {'graphic': graphic})


# impressions chart
def impressionschart(request):
    sales_data = user_report.objects.all()
    categories = [sale.date for sale in sales_data]
    amounts = [float(sale.no_of_clicks) for sale in sales_data]
    plt.pie(amounts, labels=categories)
    plt.xlabel('impressions')
    plt.title('NO OF IMPRESSIONS IN A DAY')
    
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')
    return render(request, 'impressionschart.html', {'graphic': graphic})
