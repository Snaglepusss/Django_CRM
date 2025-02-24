from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record


# Create your views here.
def home(request):
	records = Record.objects.all()
      
	# Check to see if logging in
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		# Authenticate
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			messages.success(request, "You Have Been Logged In!")
			return redirect('home')
		else:
			messages.success(request, "There Was An Error Logging In, Please Try Again...")
			return redirect('home')
	else:
		return render(request, 'home.html', {'records':records})

def logout_user(request): ## This is the logout page
    logout(request)
    messages.success(request, "You have been logged out...")
    return redirect('home')

def register_user(request): ## This is the register page function
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Authenticate and login user
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, "You have successfully registered")
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form': form})
    return render(request, 'register.html', {'form': form})

def customer_record(request, pk): # Customer Record Function
	if request.user.is_authenticated: # Check if user is logged in
		# Look Up Records
		customer_record = Record.objects.get(id=pk)
		return render(request, 'record.html', {'customer_record':customer_record})
	else:
		messages.success(request, "You Must Be Logged In To View That Page...")
		return redirect('home')
	
def delete_record(request, pk): # Delete Record Function
	if request.user.is_authenticated: # Check if user is logged in
		delete_it = Record.object.get(id=pk)
		delete_it.delete()
		messages.success(request, "Record Deleted...")
		return redirect('home')
	else:
		messages.success(request, "You Must Be Logged In To View That Page...")
		return redirect('home')
    
def edit_record(request, pk): # Edit Record Function
	if request.user.is_authenticated:
		record = Record.objects.get(id=pk)  # Get Record
		form = AddRecordForm(instance=record) # Create Form
		if request.method == 'POST':
			form = AddRecordForm(request.POST, instance=record)
			if form.is_valid():
				form.save()
				messages.success(request, "Record Updated...")
				return redirect('home')
		return render(request, 'edit_record.html', {'form':form})
	else:
		messages.success(request, "You Must Be Logged In To View That Page...")
		return redirect('home')

def add_record(request):
	form = AddRecordForm(request.POST or None)
	if request.user.is_authenticated:
		if request.method == "POST":
			if form.is_valid():
				add_record = form.save()
				messages.success(request, "Record Added...")
				return redirect('home')
		return render(request, 'add_record.html', {'form':form})
	else:
		messages.success(request, "You Must Be Logged In...")
		return redirect('home')

    