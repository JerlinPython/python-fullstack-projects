from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from.import views


urlpatterns=[

    path("",views.saveit,name="saveit"),
    path("basic",views.basic_data,name="basic_data"),
    path("edu",views.education_data,name="education_data"),
    path("files",views.files_upload,name="files_upload"),
    path("fin",views.financial_data,name="financial_data"),
    path("medical",views.medical_data,name="medical_data"),
    path("signup",views.sign_up,name="sign_up"),
    path("emp",views.employe_data,name="employe_data"),
    path("basic1",views.basic_show,name="basic_show"),
    path("edu1",views.edu_show,name="edu_show"),
    path("emp1",views.emp_show,name="emp_show"),
    path("files1",views.file_show,name="file_show"),
    path("medical1",views.medi_show,name="medi_show"),
    path("fin1",views.fin_show,name="fin_show"),
    path("finland",views.fin_land,name="fin_land"),
    path("fileland",views.file_land,name="file_land"),
    path("eduland",views.edu_land,name="edu_land"),
    path("empland",views.emp_land,name="emp_land"),
    path("medicalland",views.medical_land,name="medical_land"),
    path("basicland",views.basic_land,name="basic_land"),
    path("datas",views.datas,name="datas"),
    path("update/<id1>",views.basic_update,name="basic_update"),
    path("update1/<id1>",views.edu_update,name="edu_update"),
    path("update2/<id1>", views.emp_update, name="emp_update"),
    path("update3/<id1>", views.medi_update, name="medi_update"),
    path("update4/<id1>",views.fin_update,name="fin_update"),
    path("update5/<id1>",views.file_update,name="file_update"),
    path("logout",views.lout,name="lout"),
    path("del/<id1>",views.delete,name="delete"),
    path("del1/<id1>", views.delete1, name="delete1"),
    path("del2/<id1>", views.delete2, name="delete2"),
    path("del3/<id1>", views.delete3, name="delete3"),
    path("del4/<id1>", views.delete4, name="delete4"),
    path("del5/<id1>", views.delete5, name="delete5"),
    path("home",views.saveit,name="saveit")



]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)