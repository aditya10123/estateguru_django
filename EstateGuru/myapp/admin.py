from django.contrib import admin
from.models import property_cat,property,book,property_rent,booking,customer_details,Feedback,rent
# Register your models here.
'''
from.models import property_cat,property
admin.site.register(property_cat)
admin.site.register(property)
'''
@admin.register(property_cat)
class adminprop(admin.ModelAdmin):
    list_display=['p_name','image']
# admin.site.register(property_cat,adminprop)

class properties(admin.ModelAdmin):
    list_display=[ 'pro_name','pro_address','pro_price','description', 'image','image2','image3', 'image4', 'bedrooms','bathrooms','carpet_area','deposite_amount']

admin.site.register(property,properties)


class bookadmin(admin.ModelAdmin):
    list_display=['uid','pid']
admin.site.register(book,bookadmin)

class rentadmin(admin.ModelAdmin):
    list_display=['uid','pid']
admin.site.register(rent,rentadmin)


class rentadmin(admin.ModelAdmin):
    list_display=['title','description','image','image2','image3','image4','price','location','bedrooms','bathrooms','carpet_area','date_listed','available']
admin.site.register(property_rent,rentadmin)


class bookadmin(admin.ModelAdmin):
    list_display = ['customer','pro_name','quantity','price','booking_date','status'] 
admin.site.register(booking,bookadmin)


class customeradmin(admin.ModelAdmin):
     list_display = ['user','Name','address','city','pincode']
admin.site.register(customer_details,customeradmin)

class feedbackadmin(admin.ModelAdmin):
     list_display = ['name','email','message','created_at']
admin.site.register(Feedback,feedbackadmin)


