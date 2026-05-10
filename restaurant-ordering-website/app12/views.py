from django.shortcuts import render, redirect
from app12.models import signup, reserv, Foodtable, Carttable,Billtable
from django.http import HttpResponse
from django.db.models import Q


# Create your views here.
def dishhome (request):

    return render(request,"dishdiscovery.html")


def login(request):
    if request.method == "POST":
        name = request.POST["name1"]
        password = request.POST["name2"]

        try:
            login = signup.objects.get(Username=name)


            if login.Password == password:
                request.session["member_id"] = login.id

                return render(request, "welcome1.html")
            else:
                return HttpResponse("Incorrect Password")

        except signup.DoesNotExist:
            return HttpResponse("Username not Found")

    return render(request,"dishlogin.html")


def dishabout(request):
    return render(request,"dishdiscoveryaboutus.html")


def dishreserv(request):
    if request.method=="POST":
        a=request.POST["name1"]
        b=request.POST["name2"]
        c=request.POST["name3"]
        d=request.POST["name4"]
        e=request.POST["name5"]
        j=reserv(Firstname=a,Date=b,Time=c,People=d,Phone=e)
        j.save()
        return render(request,"reservnotifi.html")
    return render(request,"dishdiscoveryreservation.html")

def dishsign(request):
    if request.method=="POST":
        a=request.POST["name1"]
        b=request.POST["name2"]
        c=request.POST["name3"]
        phone = request.POST["name4"]
        address = request.POST["name5"]


        j=signup(Username=a,Email=b,Password=c,Phone=phone,Address=address)
        j.save()
        return render(request,"welcome.html")
    return render(request,"dishdiscoverysignup.html")

def dishgallery(request):
    return render(request,"dishdiscoverygallery.html")




def item(request):
    a=Foodtable.objects.all()
    return render(request,"order.html",{"orderkey":a})

def orderinfo(request,id1):
    a=Foodtable.objects.filter(id=id1).first()
    return render(request,"orderpage.html",{"infokey":a})

def orderland(request):
    return render(request,'orderlandpage.html')


def ordercart(request):
    return render(request,"ordercart.html")



def usercart(request, id4, id5, id):
    Pid = id4
    Fname = id5
    Price = id

    if request.method == "POST":
        c = request.POST["name1"]
        total = int(c) * int(Price)
        q = Carttable(Productid=Pid, Foodname=Fname, Quantity=c, price=total, Userid=request.session["member_id"])
        q.save()
        a = Billtable(Productid=Pid, Foodname=Fname, Quantity=c, price=total, Userid=request.session["member_id"])
        a.save()
        # Render the success template instead of redirecting
        return render(request, "shopping.html")

    return render(request, "cart.html")

def usercartdata(request):
    a = Carttable.objects.filter(Userid=request.session["member_id"])
    x=0
    if a:
        for i in a:
            p=i.price
            x=x+p
            pid=i.Productid
            q=i.Quantity
            c=i.id

        return render(request, "ordercart.html",{"usercartdatakey":a,"sum":x,"Productid":pid,"Quantity":q,"id":c})
    else:
        return HttpResponse("Cart is empty")

def delete(request,id1):
    delete=Carttable.objects.get(id=id1)
    delete.delete()

    return HttpResponse("Your Item Remove Successfully")

def search(request):
    if request.method=="POST":
        a=request.POST["name1"]
        q=Foodtable.objects.filter(Q(Foodname__icontains=a))
        if not q:
            return HttpResponse("no search result")
    return render(request,"order.html",{"foodsearchkey":q})

def payment(request):
    a = Carttable.objects.filter(Userid=request.session["member_id"])
    x = 0
    for i in a:
        p = i.price
        x = x + p

    return render(request, "payment.html", {"sum": x, "id_new": request.session["member_id"]})

def success(request):
    return render(request,"order_success.html")


def catering(request):
    return render(request,"dishcatering.html")

def chinesemenu(request):
    return render(request,"chinesemenu.html")

def coffemenu(request):
    return render(request,"coffemenu.html")

def dessertmenu(request):
    return render(request,"dessertmenu.html")

def drinkmenu(request):
    return render(request,"drinkmenu.html")

def indiamenu(request):
    return render(request,"indianmenu.html")

def italymenu(request):
    return render(request,"italymenu.html")
