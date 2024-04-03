from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView,CreateView,View,UpdateView,DeleteView
from .forms import InventoryForm, UserRegistration
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login,logout
from .models import Inventory,Category
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from inventory.settings import LOW_QUANTITY


# Create your views here.
class INDEX(TemplateView):
    template_name='inventory/index.html'




class Dashboard(LoginRequiredMixin,View):
    def get(self,request):
        item=Inventory.objects.filter(user=self.request.user.id).order_by('id')
        low_inventory = Inventory.objects.filter(
			user=self.request.user.id,
			quantity__lte=LOW_QUANTITY
		)
        
        if low_inventory.count() > 0:
            if low_inventory.count() > 1:
                messages.error(request, f'{low_inventory.count()} items have low inventory')
            else:
                messages.error(request, f'{low_inventory.count()} item has low inventory')
        
        low_inventory_ids = Inventory.objects.filter(
			user=self.request.user.id,
			quantity__lte=LOW_QUANTITY
		).values_list('id', flat=True)

        return render(request, 'inventory/Dashboard.html', {'items': item, 'low_inventory_ids': low_inventory_ids})



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
    
class AddItem(LoginRequiredMixin, CreateView):
	model = Inventory
	form_class = InventoryForm
	template_name = 'inventory/item_form.html'
	success_url = reverse_lazy('dashboard')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['categories'] = Category.objects.all()
		return context

	def form_valid(self, form):
		form.instance.user = self.request.user
		return super().form_valid(form)


class EditItem(LoginRequiredMixin, UpdateView):
	model = Inventory
	form_class = InventoryForm
	template_name = 'inventory/item_form.html'
	success_url = reverse_lazy('dashboard')
     
class DeleteItem(LoginRequiredMixin, DeleteView):
	model = Inventory
	template_name = 'inventory/delete_item.html'
	success_url = reverse_lazy('dashboard')
	context_object_name = 'item'
   