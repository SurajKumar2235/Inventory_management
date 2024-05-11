from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView,CreateView,View,UpdateView,DeleteView
from .forms import InventoryForm, StockForm, UserRegistration
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login,logout
from .models import Inventory,Category
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from inventory.settings import LOW_QUANTITY
from transactions.models import PurchaseBill,SaleBill
from .models import Inventory as Stock



# Create your views here.
class INDEX(TemplateView):
    template_name='inventory/index.html'

class HomeView(View):
    template_name = "home.html"
    def get(self, request):        
        labels = []
        data = []        
        stockqueryset = Stock.objects.filter(is_deleted=False).order_by('-quantity')
        for item in stockqueryset:
            labels.append(item.name)
            data.append(item.quantity)
        sales = SaleBill.objects.order_by('-time')[:3]
        purchases = PurchaseBill.objects.order_by('-time')[:3]
        context = {
            'labels'    : labels,
            'data'      : data,
            'sales'     : sales,
            'purchases' : purchases
        }
        return render(request, self.template_name, context)


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
     


# Import necessary modules
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Inventory, inventory_History
from .serializers import InventoryHistorySerializer

# Define a viewset for selling items
class SellItemViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)  # Require authentication for selling items

    def create(self, request):
        # Extract data from the request
        item_id = request.data.get('item_id')
        qty_sold = request.data.get('qty_sold')
        
        # Extract employee_id from the JWT payload
        employee_id = request.user.id

        try:
            # Retrieve the inventory item
            inventory_item = Inventory.objects.get(pk=item_id)
            
            # Check if the requested quantity is available
            if inventory_item.quantity < qty_sold:
                return Response({"error": "Insufficient quantity available"}, status=status.HTTP_400_BAD_REQUEST)
            
            # Reduce the quantity in the inventory
            inventory_item.quantity -= qty_sold
            inventory_item.save()
            
            # Create a new entry in the inventory history
            inventory_history = inventory_History.objects.create(
                item_name=inventory_item.name,
                item=inventory_item,
                qty_purchased=qty_sold,
                price=inventory_item.category,  # Assuming price is stored in category
                employee_id=employee_id
            )

            # Serialize the inventory history data
            serializer = InventoryHistorySerializer(inventory_history)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Inventory.DoesNotExist:
            return Response({"error": "Inventory item not found"}, status=status.HTTP_404_NOT_FOUND)

   

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

@login_required
def employee_list(request):
    employees = User.objects.filter(is_staff=True)  # Assuming staff users are employees
    return render(request, 'employee_list.html', {'employees': employees})

@login_required
def employee_detail(request, employee_id):
    employee = User.objects.get(id=employee_id)
    return render(request, 'employee_detail.html', {'employee': employee})


from django.shortcuts import render
from .models import Employees

def employee_view(request):
  # Check user permissions (if needed)
  if request.user.is_authenticated and request.user.is_staff:  # Assuming staff has employee access
    employees = Employees.objects.all()  # Get all employees
  else:
    employees = None  # Restrict access if not authorized

  context = {'employees': employees}
  return render(request, 'employee_template.html', context)

from .filters import StockFilter
from django_filters.views import FilterView

class StockListView(FilterView):
    filterset_class = StockFilter
    queryset = Stock.objects.filter(is_deleted=False)
    template_name = 'inventory.html'
    paginate_by = 10

from django.contrib.messages.views import SuccessMessageMixin


class StockCreateView(SuccessMessageMixin, CreateView):                                 # createview class to add new stock, mixin used to display message
    model = Stock                                                                       # setting 'Stock' model as model
    form_class = StockForm                                                              # setting 'StockForm' form as form
    template_name = "edit_stock.html"                                                   # 'edit_stock.html' used as the template
    success_url = '/inventory'                                                          # redirects to 'inventory' page in the url after submitting the form
    success_message = "Stock has been created successfully"                             # displays message when form is submitted

    def get_context_data(self, **kwargs):                                               # used to send additional context
        context = super().get_context_data(**kwargs)
        context["title"] = 'New Stock'
        context["savebtn"] = 'Add to Inventory'
        return context       
    
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
import numpy as np
import joblib
from statsmodels.tsa.statespace.sarimax import SARIMAX
from datetime import datetime, timedelta

@csrf_exempt
def predict(request):
    if request.method == 'POST':
        # Load the trained SARIMAX model
        model = joblib.load('Sarimax.pkl')

        # Get input data from request.POST or request.body
        today = datetime.now().date()
        initial_inventory = float(request.POST.get('initial_inventory'))
        lead_time = int(request.POST.get('lead_time'))
        service_level = float(request.POST.get('service_level'))
        
        # Preprocess input data if necessary
        # For example, create a DataFrame with the input parameters
        input_data = pd.DataFrame({
            'date': [today],
            'initial_inventory': [initial_inventory],
            'lead_time': [lead_time],
            'service_level': [service_level]
        })
        df=pd.read_csv('archive/train.csv')
        df=df[df['store']==1]
        df=df[df['item']==1]
        print(df)
        start_date = df.index[0]
        end_date = df.index[-1]
        exog_features = ['store']
        df=df[:lead_time]
        # Perform prediction
        prediction = model.predict(len(df), len(df) + lead_time - 1,exog=df[exog_features])
        print(prediction)

        # Create date indices for the future predictions
        future_dates = pd.date_range(start=prediction.index[-1] + pd.DateOffset(days=1), periods=lead_time, freq='D')

        # Create a pandas Series with the predicted values and date indices
        forecasted_demand = pd.Series(prediction, index=future_dates)

        # Calculate the optimal order quantity using the Newsvendor formula
        z = np.abs(np.percentile(forecasted_demand, 100 * (1 - service_level)))
        order_quantity = np.ceil(forecasted_demand.mean() + z).astype(int)

        # Calculate the reorder point
        reorder_point = forecasted_demand.mean() * lead_time + z

        # Calculate the optimal safety stock
        safety_stock = reorder_point - forecasted_demand.mean() * lead_time

        # Calculate the total cost (holding cost + stockout cost)
        holding_cost = 0.1  # it's different for every business, 0.1 is an example
        stockout_cost = 10  # it's different for every business, 10 is an example
        total_holding_cost = holding_cost * (initial_inventory + 0.5 * order_quantity)
        total_stockout_cost = stockout_cost * np.maximum(0, forecasted_demand.mean() * lead_time - initial_inventory)

        # Calculate the total cost
        total_cost = total_holding_cost + total_stockout_cost

        # Return prediction and additional metrics as JSON response
        return JsonResponse({
            'prediction': prediction.tolist(),
            'order_quantity': order_quantity,
            'reorder_point': reorder_point,
            'safety_stock': safety_stock,
            'total_cost': total_cost
        })

    else:
        return JsonResponse({'error': 'Only POST requests are allowed'})
