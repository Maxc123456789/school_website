from django.shortcuts import render, redirect, get_object_or_404
from .models import Student
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'students/home.html')

def student_list(request):
    students = Student.objects.all()
    return render(request, 'students/student_list.html', {'students': students})

def add_student(request):
    if request.method == 'POST':
        Student.objects.create(
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            age=request.POST['age'],
            email=request.POST['email'],
            date_of_birth=request.POST['date_of_birth']
        )
        return redirect('student_list')
    return render(request, 'students/add_student.html')

def edit_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        student.first_name = request.POST['first_name']
        student.last_name = request.POST['last_name']
        student.age = request.POST['age']
        student.email = request.POST['email']
        student.date_of_birth = request.POST['date_of_birth']
        student.save()
        return redirect('student_list')
    return render(request, 'students/edit_student.html', {'student': student})

def delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    student.delete()
    return redirect('student_list')

def signup_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm = request.POST['confirm']

        if password != confirm:
            messages.error(request, "Passwords do not match!")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
            return redirect('signup')

        User.objects.create_user(username=username, password=password)
        messages.success(request, "Account created successfully! Please log in.")
        return redirect('login')

    return render(request, 'students/signup.html')


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {username}!")
            return redirect('student_list')
        else:
            messages.error(request, "Invalid username or password")
            return redirect('login')

    return render(request, 'students/login.html')


def logout_user(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')

@login_required(login_url='login')
def student_list(request):
    students = Student.objects.all()
    return render(request, 'students/student_list.html', {'students': students})


@login_required(login_url='login')
def add_student(request):
    if request.method == 'POST':
        Student.objects.create(
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            age=request.POST['age'],
            email=request.POST['email'],
            date_of_birth=request.POST['date_of_birth']
        )
        return redirect('student_list')
    return render(request, 'students/add_student.html')


@login_required(login_url='login')
def edit_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        student.first_name = request.POST['first_name']
        student.last_name = request.POST['last_name']
        student.age = request.POST['age']
        student.email = request.POST['email']
        student.date_of_birth = request.POST['date_of_birth']
        student.save()
        return redirect('student_list')
    return render(request, 'students/edit_student.html', {'student': student})


@login_required(login_url='login')
def delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    student.delete()
    return redirect('student_list')

def about(request):
    return render(request, 'students/about.html')

def contact(request):
    return render(request, 'students/contact.html')
