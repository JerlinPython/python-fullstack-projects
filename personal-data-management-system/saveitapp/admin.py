from django.contrib import admin

# Register your models here.

from saveitapp.models import signup,basicdata,educationdata,financialdata,employedata,medicaldata,filedata

admin.site.register(signup)
admin.site.register(basicdata)
admin.site.register(educationdata)
admin.site.register(financialdata)
admin.site.register(employedata)
admin.site.register(medicaldata)
admin.site.register(filedata)


