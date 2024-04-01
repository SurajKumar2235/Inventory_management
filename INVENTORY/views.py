from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import TemplateView
from .forms import UserRegistration
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login,logout
# Create your views here.
class INDEX(TemplateView):
    template_name='inventory/index.html'




class Dashboard(View):
    def get(self,request):
        return render(request,'inventory/Dashboard.html')


class signUpView(View):
    def get(self,request):

        form=UserRegistration()
        return render(request,'inventory/signup.html',{'form':form})



    def post(self,request):
        print(request)
        form=UserRegistration(request.POST)
        if form.is_valid():
            form.save()
            user=authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1']
            )

            login(request,user)

            return redirect('index_page')
        
        print("error")
        form=UserRegistration()
        return render(request,'inventory/signup.html',{'form':form})


class LogoutView(View):
    def get(self, request):
        logout(request)  # Logout the current user
        return render(request, 'inventory/logout.html')


   