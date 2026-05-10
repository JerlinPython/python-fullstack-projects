from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


from.import views

urlpatterns=[path("",views.dishhome,name="dishhome"),
             path("about",views.dishabout,name="dishabout"),
             path("sign",views.dishsign,name="dishsign"),
             path("login",views.login,name="login"),
             path("reserve",views.dishreserv,name="dishreserve"),
             path("gallery",views.dishgallery,name="dishgallery"),
             path("order",views.item,name="item"),
             path("orderinfo/<str:id1>",views.orderinfo,name="orderinfo"),
             path('landpage',views.orderland,name="orderland"),
             path("ocart",views.ordercart,name="ordercart"),
             path("path15/<id4>,<id5>,<id>", views.usercart, name="usercart"),
             path("path16", views.usercartdata, name="usercartdata"),
             path("del/<id1>",views.delete,name="delete"),
             path("search",views.search,name="search"),
             path("payment",views.payment,name="payment"),
             path("success",views.success,name="success"),
             path("catering",views.catering,name="catering"),
             path("chinesemenu",views.chinesemenu,name="chinesemenu"),
             path("coffemenu", views.coffemenu, name="coffemenu"),
             path("dessertmenu", views.dessertmenu, name="dessertmenu"),
             path("drinkmenu", views.drinkmenu, name="drinkmenu"),
             path("indiamenu", views.indiamenu, name="indiamenu"),
             path("italymenu", views.italymenu, name="italymenu")





]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)