from math import degrees
from django.shortcuts import render,redirect
from django.contrib.auth import logout
from django.template.context_processors import request
from sqlparse.sql import Comment

from saveitapp.models import signup, basicdata, educationdata, financialdata,employedata,medicaldata,filedata


# Create your views here.
def home(request):
    return render(request,"saveit.html")
def saveit(request):
    if request.method == "POST":
        name = request.POST["name1"]
        password = request.POST["name2"]

        try:
            logindata = signup.objects.get(Name=name)

            if logindata.Password == password:
                request.session["member_id"] = logindata.id
                return render(request, "loginnoti.html")
            else:
                return render(request, "password.html")

        except signup.DoesNotExist:

            return render(request, "username.html")
    return render(request,"saveit.html")

def basic_data(request):

    if request.method=="POST":
        name=request.POST["name1"]
        age=request.POST["name2"]
        phone=request.POST["name3"]
        email=request.POST["name4"]
        gender=request.POST["gender"]
        dob=request.POST["name5"]

        b_data=basicdata(Name=name,Age=age,Phone=phone,Email=email,Gender=gender,Date=dob)
        b_data.save()
        return render(request, "datasaved.html")

    return render(request,"basic_data.html")

def education_data(request):

    if request.method=="POST":
        name=request.POST["name1"]
        school=request.POST["name2"]
        course=request.POST["name3"]
        degree=request.POST["name4"]
        resource=request.POST["name5"]

        edu_data=educationdata(Name=name,School=school,Course=course,Degree=degree,Resource=resource)
        edu_data.save()

        return render(request, "datasaved4.html")

    return render(request,"education_data.html")


def files_upload(request):

    if request.method=="POST":
        name=request.POST["name1"]
        marksheet=request.FILES["name2"]
        degree=request.FILES["name3"]
        passport=request.FILES["name4"]
        medical=request.FILES["name5"]
        work=request.FILES["name6"]
        file=filedata(Name=name,Marksheet=marksheet,Degree=degree,Passport=passport,Medical=medical,Work=work)
        file.save()

        return render(request, "datasaved5.html")


    return render(request,"files_upload.html")

def financial_data(request):

    if request.method=="POST":
        name=request.POST["name1"]
        bank=request.POST["name2"]
        account=request.POST["name3"]
        ifsc=request.POST["name4"]

        fin_data=financialdata(Name=name,Bank=bank,Account=account,Ifsc=ifsc)
        fin_data.save()

        return render(request, "datasaved1.html")

    return render(request,"financial_data.html")

def medical_data(request):

    if request.method=="POST":
        name=request.POST["name1"]
        age=request.POST["name2"]
        height=request.POST["name3"]
        weight=request.POST["name4"]
        health=request.POST["name5"]

        med_data=medicaldata(Name=name,Age=age,Height=height,Weight=weight,Health=health)

        med_data.save()

        return render(request, "datasaved2.html")

    return render(request,"medical_data.html")


def employe_data(request):
    if request.method=="POST":

        name=request.POST["name1"]
        empid=request.POST["name2"]
        company=request.POST["name3"]
        field=request.POST["name4"]
        experience=request.POST["name5"]

        emp_data=employedata(Name=name,Employeid=empid,Company=company,Field=field,Experience=experience)
        emp_data.save()

        return render(request,"datasaved3.html")
    return render(request,"employedata.html")

def sign_up(request):
    if request.method=="POST":

        name=request.POST["name1"]
        gmail=request.POST["name2"]
        password=request.POST["name3"]
        signupdata=signup(Name=name,Gmail=gmail,Password=password)

        signupdata.save()

        return render(request,"signupnoti.html")

    return render(request,"signup.html")


def basic_show(request):
    b_show=basicdata.objects.all()
    return render(request,"basic_show.html",{"basickey":b_show})

def edu_show(request):
    e_show=educationdata.objects.all()
    return render(request,"edu_show.html",{"edukey":e_show})

def emp_show(request):
    em_show=employedata.objects.all()
    return render(request,"emp_show.html",{"empkey":em_show})

def fin_show(request):
    f_show=financialdata.objects.all()
    return render(request,"fin_show.html",{"finkey":f_show})

def medi_show(request):
    m_show=medicaldata.objects.all()
    return render(request,"medi_show.html",{"medikey":m_show})

def file_show(request):
    fi_show=filedata.objects.all()
    return render(request,"file_show.html",{"filekey":fi_show})

def fin_land(request):
    return render(request,"financial_land.html")

def file_land(request):
    return render(request,"file_land.html")

def emp_land(request):
    return render(request,"emp_land.html")

def edu_land(request):
    return render(request,"edu_land.html")
def basic_land(request):
    return render(request,"basic_land.html")
def medical_land(request):
    return render(request,"medical_land.html")

def datas(request):
    return render(request,"datas.html")

def basic_update(request,id1):
    b_update=basicdata.objects.get(id=id1)
    if request.method=="POST":
        b_update.Name=request.POST["name1"]
        b_update.Age=request.POST["name2"]
        b_update.Phone=request.POST["name3"]
        b_update.Email=request.POST["name4"]
        b_update.Gender=request.POST["gender"]
        b_update.Date=request.POST["name5"]

        b_update.save()
        return render(request, "update.html")
    return render(request,"basic_update.html",{"bupdatekey":b_update})

def edu_update(request,id1):
    e_update=educationdata.objects.get(id=id1)
    if request.method == "POST":
        e_update.Name = request.POST["name1"]
        e_update.School = request.POST["name2"]
        e_update.Course = request.POST["name3"]
        e_update.Degree = request.POST["name4"]
        e_update.Resource=request.POST["name5"]
        e_update.save()

        return render(request, "update.html")
    return render(request, "edu_update.html", {"edudatekey": e_update})


def emp_update(request,id1):
    em_update = employedata.objects.get(id=id1)
    if request.method == "POST":
        em_update.Name = request.POST["name1"]
        em_update.Employeid = request.POST["name2"]
        em_update.Company = request.POST["name3"]
        em_update.Field= request.POST["name4"]
        em_update.Experience = request.POST["name5"]
        em_update.save()


        return render(request, "update.html")

    return render(request, "emp_update.html", {"empdatekey": em_update})


def medi_update(request,id1):
    m_update=medicaldata.objects.get(id=id1)
    if request.method == "POST":
        m_update.Name = request.POST["name1"]
        m_update.Age = request.POST["name2"]
        m_update.Height = request.POST["name3"]
        m_update.Weight= request.POST["name4"]
        m_update.Health = request.POST["name5"]
        m_update.save()

        return render(request, "update.html")
    return render(request, "medical_update.html", {"medicalkey": m_update})

def fin_update(request,id1):
    f_update=financialdata.objects.get(id=id1)
    if request.method == "POST":
        f_update.Name = request.POST["name1"]
        f_update.Bank = request.POST["name2"]
        f_update.Account = request.POST["name3"]
        f_update.Ifsc = request.POST["name4"]

        f_update.save()

        return render(request, "update.html")
    return render(request, "fin_update.html", {"finkey": f_update})


def file_update(request,id1):
    fi_update=filedata.objects.get(id=id1)
    if request.method=="POST":
        fi_update.Name=request.POST["name1"]

        if 'change_image' in request.POST:
            fi_update.Marksheet=request.FILES["name2"]
            fi_update.Degree=request.FILES["name3"]
            fi_update.Passport=request.FILES["name4"]
            fi_update.Medical=request.FILES["name5"]
            fi_update.Work=request.FILES["name6"]

            fi_update.save()


        return render(request, "update.html")
    return render(request,"file_update.html",{"filekey":fi_update})

def lout(request):
    logout(request)
    return redirect('datas')

def delete(request,id1):
    delete=basicdata.objects.get(id=id1)
    delete.delete()

    return render(request,"delete.html")


def delete1(request, id1):
    delete = educationdata.objects.get(id=id1)
    delete.delete()

    return render(request, "delete.html")


def delete2(request, id1):
    delete = employedata.objects.get(id=id1)
    delete.delete()

    return render(request, "delete.html")


def delete3(request, id1):
    delete = medicaldata.objects.get(id=id1)
    delete.delete()

    return render(request, "delete.html")


def delete4(request, id1):
    delete = financialdata.objects.get(id=id1)
    delete.delete()

    return render(request, "delete.html")


def delete5(request, id1):
    delete = filedata.objects.get(id=id1)
    delete.delete()

    return render(request, "delete.html")










