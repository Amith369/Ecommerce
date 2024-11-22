from django.shortcuts import render,redirect
from django.views.generic import View,TemplateView,CreateView,DeleteView,DetailView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib import messages

from store.models import Product,BasketItem,Size,Order
from store.forms import RegistrationFrom,LoginForm
from store.decorators import sigin_required,owner_permission_required



# url: localhost:8000/register/
# methods: get,post
# form_class:RegistrationForm

class SignUpView(CreateView):

    form_class=RegistrationFrom
    template_name="login.html"
    model=User



# url: localhost:8000/
# methods: get,post
# form_class:loginform
class SignInView(View):

    def get(self,request,*args,**kwargs):
        form=LoginForm()
        return render(request,"login.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            u_name=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            user_object=authenticate(request,username=u_name,password=pwd)
            if user_object:
                login(request,user_object)
            return redirect("index")
        messages.error(request,"invalid credentials")
        return render(request,"login.html",{"form":form})



# views>generic>View,TemplateView,FromView,CreateView,ListView,DetailView,UpdateView,DeleteView
@method_decorator(sigin_required,name="dispatch")
class IndexView(TemplateView):

        def get(self,request,*args,**kwargs):
            qs=Product.objects.all()
            return render(request,"index.html",{"data":qs})



# url: localhost:8000/product/{id}/
@method_decorator(sigin_required,name="dispatch")
class ProductDetailView(DetailView):
#  we can implement these two Views both are same
#  
     def get(self,request,*args,**kwargs):
          id=kwargs.get("pk")
          qs=Product.objects.get(id=id)
          return render(request,"product_detail.html",{"data":qs})
     
    #  template_name="product_detail.html"
    #  model=Product
    #  context_object_name="data"



class HomeView(TemplateView):
     template_name="base.html"
     


# add to basket
# url:localhost:8000/products/{id}/add_to_basket/
# method:post
@method_decorator(sigin_required,name="dispatch")
class AddToBasketView(View):
     
     def post(self,request,*args,**kwargs):
          size=request.POST.get("size")
          size_obj=Size.objects.get(name=size)
          qty=request.POST.get("qty")
          id=kwargs.get("pk")
          product_obj=Product.objects.get(id=id)
          BasketItem.objects.create(
               size_object=size_obj,
               qty=qty,
               product_object=product_obj,
               basket_object=request.user.cart
          )
          return redirect("index")


# basket item list view
# url:localhost:8000/basket/item/all/
# method:get
@method_decorator(sigin_required,name="dispatch")
class BasketItemListView(View):
     
    def get(self,request,*args,**kwargs):
        qs=request.user.cart.cartitem.filter(is_order_placed=False)
        return render(request,"cart.html",{"data":qs})


# basket_item remove
# localhost:8000/basket/items/{id}/remove/
@method_decorator([sigin_required,owner_permission_required],name="dispatch")
class BasketItemRemoveView(View):
     
     def get(self,request,*args,**kwargs):
          id=kwargs.get("pk")
          basket_item_object=BasketItem.objects.get(id=id)
          basket_item_object.delete()
          return redirect("basket-items")


# localhost:8000/basket/items/{id}/change/
@method_decorator([sigin_required,owner_permission_required],name="dispatch")
class CartItemUpdateQuantityView(View):
     
    def post(self,request,*args,**kwargs):
        action=request.POST.get("counterButton")
        print(action)
        id=kwargs.get("pk")
        basket_item_object=BasketItem.objects.get(id=id)
        if action=="+":
           basket_item_object.qty+=1    
           basket_item_object.save()
        else:
            basket_item_object.qty-=1    
            basket_item_object.save()                     
        return redirect("basket-items")


class CheckOutView(View):

    
    def get(self,request,*args,**kwargs):
        return render(request,"checkout.html")
    
    def post(self,request,*args,**kwargs):
        email=request.POST.get("email")
        phone=request.POST.get("phone")
        address=request.POST.get("address")
        print(email,phone,address)
        return redirect("index")


@method_decorator([sigin_required,never_cache],name="dispatch")
class SignOutView(View):

    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("signin")
    

class OrderSummaryView(View):

    def get(self,request,*args,**kwargs):
        qs=Order.objects.filter(user_object=request.user)
        return render(request,"order_summary.html",{"data":qs})
