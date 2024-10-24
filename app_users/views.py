from django.shortcuts import render
from django.http import HttpRequest , HttpResponseRedirect
from django.contrib.auth import login
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode , urlsafe_base64_decode
from django.utils.encoding import force_bytes
from app_users.forms import UserProfileForm , ExtendedProfileForm
from app_users.models import CustomUser
from app_users.utils.activation_token_generator import activation_token_generator
from app_users.forms import RegisterForm


def register(request : HttpRequest):
    #POST
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Register user
            user : CustomUser = form.save(commit=False)
            user.is_active = False
            user.save()
            # login(request , user)
            # build email body html
            context = {
                "protocol" : request.scheme,
                "host" : request.get_host(),
                "uidb64" : urlsafe_base64_encode(force_bytes(user.id)),
                "token" : activation_token_generator.make_token(user)
            }
            email_body = render_to_string("app_users/activate_email.html" , context)
            # sent email
            email = EmailMessage(
                to = [user.email] , 
                subject = "Pls activate your account" , 
                body = email_body
            )
            email.send()

            return HttpResponseRedirect(reverse("register_thankyou"))
    else:
        form = RegisterForm()

    context = {"form" : form}
    return render(request , "app_users/register.html",context)


def register_thankyou(request : HttpRequest):
    return render(request , "app_users/register_thankyou.html")


def activate(request : HttpRequest , uidb64: str , token: str ):
    title = "Activate Account Success"
    description = "สามารถเข้าสู่ระบบได้เลย"
    # decode user id
    id = urlsafe_base64_decode(uidb64).decode()
    try:
        user : CustomUser = CustomUser.objects.get(id=id)
        if not activation_token_generator.check_token(user , token):
            raise Exception("Check token false")
        user.is_active = True
        user.save()
    except:
        print("Activate ไม่ผ่าน")
        title = "Activate Account Fail"
        description = "ลิงค์อาจถูกใช้ไปแล้ว หรือหมดอายุ"

    context = {"title" : title , "description" : description}
    return render(request , "app_users/activate.html" , context)

@login_required
def dashboard(request : HttpRequest):
    return render(request , "app_users/dashboard.html")

@login_required
def profile(request : HttpRequest):
    user = request.user

    #POST
    if request.method == 'POST':
        form = UserProfileForm(request.POST , instance = user)
        is_new_profile = False

        try:
            # Will update
            extended_form = ExtendedProfileForm(request.POST , instance = user.profile)
        except:
            # Will create
            extended_form = ExtendedProfileForm(request.POST)
            is_new_profile = True



        if form.is_valid() and extended_form.is_valid():
            form.save()
            if is_new_profile:
                # create
                profile = extended_form.save(commit = False)
                profile.user = user
                profile.save()
            else:
                # update
                extended_form.save()

            response = HttpResponseRedirect(reverse("profile"))
            response.set_cookie("is_saved" , "1")
            return response
    else:
        form = UserProfileForm(instance = user)
        try:
            extended_form = ExtendedProfileForm(instance = user.profile)
        except:
            extended_form = ExtendedProfileForm()


    # GET
    is_saved = request.COOKIES.get("is_saved") == "1"
    flash_massage = "บันทึกเรียบร้อย" if is_saved else None
    context = {
        "form" : form , 
        "extended_form" : extended_form ,
        "flash_massage" : flash_massage,
    }
    response = render(request , "app_users/profile.html" , context)
    if is_saved :
        response.delete_cookie("is_saved")
        
    return response



