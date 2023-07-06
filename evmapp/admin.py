from django.contrib import admin
from .models import Admin,login,User,convention,GalleryImage,catering,cateringmenu,decoration,photography,PreviousWorks,accommodation,photos_collection,entertainment,transportation,Convention_Booking,Catering_Booking,Decoration_Booking,Photography_Booking,Entertainment_Booking,Accommodation_Booking,Transportation_Booking

# Register your models here.

admin.site.register(Admin)

admin.site.register(User)
admin.site.register(login)


admin.site.register(convention)
admin.site.register(GalleryImage)
admin.site.register(catering)
admin.site.register(cateringmenu)
admin.site.register(decoration)
admin.site.register(photography)
admin.site.register(PreviousWorks)
admin.site.register(accommodation)
admin.site.register(photos_collection)
admin.site.register(entertainment)
admin.site.register(transportation)

admin.site.register(Convention_Booking)
admin.site.register(Catering_Booking)
admin.site.register(Decoration_Booking)
admin.site.register(Photography_Booking)
admin.site.register(Entertainment_Booking)
admin.site.register(Accommodation_Booking)
admin.site.register(Transportation_Booking)





