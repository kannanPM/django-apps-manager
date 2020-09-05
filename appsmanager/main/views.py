from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.views import View

from django.views.generic.base import TemplateView
from main.models import App
from main.models import Subscriber

from django.contrib import auth
from django.shortcuts import redirect

from django.contrib.auth.models import User, Group

from django.core.mail import send_mail

from django.template.response import TemplateResponse
from django.http import JsonResponse



class Home(TemplateView):
    
    template_name = "home.html"

    

    def home(request):
                                
        if request.user.is_authenticated:

            userid=request.user.id

            apps = App.objects.all()
        
            allowedapps=[]
            
            for app in apps:
                # check if the user subscribed or default visibility is true

                subscriber_ds=Subscriber.objects.filter(app_id=app.id,user_id=userid)

                if app.default_visibility or subscriber_ds:
                    allowedapps.append(app)
                    

                print("App",app)            
    
            
        

            context={"apps": allowedapps}
            response = TemplateResponse(request,"home.html", context)
            return response
        else:
            
            return redirect("/main/login")


    def logout(request):
        # To logout the requested user
        print("Logging out")
        auth.logout(request)
        return redirect("/main/login")
    
    def openapp(request,appid):

        userid=request.user.id

        print(appid,userid)

        # Get app object
        app_obj_ds=App.objects.filter(id=appid)
        if not app_obj_ds:
            return redirect("/main/home")


        app_obj=app_obj_ds.get()    
    
        # Check if the user subscribed to the selected app
        subscriber_ds=Subscriber.objects.filter(app_id=appid,user_id=userid)
    
        # if not redirect to subscribe page
        if not subscriber_ds:
           

            request.session['apptosubscribe'] = {"id": app_obj.id, "name": app_obj.app_name, "description": app_obj.app_description,"url": app_obj.app_link}

            return redirect("/main/subscribe")
    
        
        else:
            subscriber_obj=subscriber_ds.get()
            
            # allow only if active
            if subscriber_obj.is_active:

                # else redirect to app page
                return redirect(app_obj.app_link)
                
            else:
                
                return redirect("/main/info")
            
     
    def getstat(request):
        # To logout the requested user
        print("getstat")

        if not request.session.has_key('counter'):
            request.session['counter']=0
        else:
            request.session['counter']+=1
    
        data = {'counter': request.session['counter']}

        

        return JsonResponse(data, safe=False)

    
       
class Subscribe(TemplateView):
        
    template_name = "subscribe.html"

    def info(request):
                
        response = TemplateResponse(request,"subscribedinfo.html")
        return response

    def subscribetoapp(request):
        userid=request.user.id
        print("User requested: ",userid)
        if request.session.has_key('apptosubscribe'):
            app_data=request.session['apptosubscribe'] 

            print("App data",app_data)
 
            subscriber_ds=Subscriber.objects.filter(app_id=app_data["id"],user_id=userid)

            # if not redirect to subscribe page
            if not subscriber_ds:

                Subscriber.objects.create(app_id_id=app_data["id"], user_id=request.user)

                # get all the admin/superuser emails
                superusers_emails = User.objects.filter(is_superuser=True).values_list('email')
            
                emails=[]

                for email in superusers_emails:
                    emails.append(email[0])
            
                
                print("Superuser emails",emails)
                #message="User (%s) successfully subscribed to the app (%s) "%(request.user.first_name+" "+request.user.last_name,str(app_data["id"])+". "+app_data["name"]) 
                message="User successfully subscribed"
                # Send mail to admins
                send_mail("Subscribed",message,"appsmanager@gmail.com",emails)

                # Redirect to app home page, once subscribed successfully
            return redirect("/main/info")
        
        else:
            return redirect("/main/home")
     
