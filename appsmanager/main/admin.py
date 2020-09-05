from django.contrib import admin

# Register your models here.

from main.models import App,Subscriber


class SubscriberAdmin(admin.ModelAdmin):
    model = Subscriber
    list_display = ('id','user_id', 'app_id', 'is_active')
    list_filter = ('is_active', )

class AppAdmin(admin.ModelAdmin):
    model = App
    list_display = ('id','app_name', 'app_description', 'default_visibility','app_link')

admin.site.register(Subscriber,SubscriberAdmin)

admin.site.register(App,AppAdmin)
