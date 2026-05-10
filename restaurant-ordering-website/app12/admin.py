from django.contrib import admin

# Register your models here.

from app12.models import signup,reserv,Foodtable,Carttable,Billtable
admin.site.register(signup)
admin.site.register(reserv)
admin.site.register(Foodtable)
admin.site.register(Carttable)
admin.site.register(Billtable)
