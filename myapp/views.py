
from django.shortcuts import render, redirect, HttpResponse
from .models import Course
from .video import Video
from .forms import RegistrationForm, LogiForm
from django.contrib.auth import logout
from django .views import View
from time import time
from .models import Contact
# Create your views here.


def home(request):
    courses = Course.objects.all()
    print(courses)
    return render(request, template_name="myapp/home.html",
    context={"courses": courses})

def about(request):
    return render(request, 'myapp/about.html')

def contact(request):
    if request.method == 'POST':
        fn = request.POST['firstname']
        ln = request.POST['lastname']
        em = request.POST['email']
        mb = request.POST['mobile']
        ms = request.POST['message']
        s = Contact(firstname=fn, lastname=ln, email=em, mobile=mb, message=ms)
        s.save()
    return render(request, 'myapp/contact.html')

def Course_page(request):
    return render(request, 'myapp/Course_page.html')

def teachers(request):
    return render(request, 'myapp/Teacher.html')

class SignupView(View):
    def get(self, request):
        form = RegistrationForm()
        return render(request, template_name='myapp/signup.html', context={'form': form})
    def post(self ,request):
        form = RegistrationForm(request.POST)
        if (form.is_valid()):
            user = form.save()
            if (user is not None):
                return redirect('login')
        return render(request, template_name='myapp/signup.html', context={'form': form})



class LoginView(View):
     def get(self,request):
         form = LogiForm()
         context = {
             "form": form
         }
         return render(request,template_name="myapp/login.html",context=context)

     def post(self, request):
         form = LogiForm(request=request, data=request.POST)
         context = {
             "form": form
         }
         if(form.is_valid()):
              return redirect('home')
         return render(request, template_name="myapp/login.html", context=context)


def CoursePage(request, slug):
    course = Course.objects.get(slug=slug)
    serial_number = request.GET.get('lecture')
    videos = course.video_set.all().order_by("serial_number")
    if serial_number is None:
        serial_number = 1
    video = Video.objects.get(serial_number=serial_number, course=course)
    if((request.user.is_authenticated is False) and (video.is_preview is False)):
        return redirect("login")
    print(video)

    context = {
        "course": course,
        "video": video,
        "videos": videos
    }
    return render(request, template_name="myapp/Course_page.html" , context=context)

def signout(request):
    logout(request)
    return redirect("home")

# checkout
import razorpay

client = razorpay.Client(auth=("rzp_test_RwBGNaCfGQbRBx", "R8vNA2XQiQACvP3q58PrxRbN"))


def checkout(request, slug):
    course = Course.objects.get(slug=slug)
    user = None
    if not request.user.is_authenticated:
        return redirect("login")
    #  i you are enrolled in this course you can watch every video
    user = request.user
    action = request.GET.get('action')
    order = None
    if action == 'create_payment':
        amount = int((course.price - (course.price * course.discount * 0.01)) * 100)
        currency = "INR"
        notes = {
            "email": user.email,
            "name": f'{user.first_name} {user.last_name}'
        }
        reciept = f"myproject-{int(time())}"
        order = client.order.create(
            {'receipt': reciept,
             'notes': notes,
             ' amount': amount,
             'currency': currency
             }
         )
    context = {
        "course": course,
        "order": order
     }
    return render(request, template_name="myapp/check-out.html", context=context)
