from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from .models import *
from django.core.mail import send_mail
from django.conf import settings
from django.core.files.storage import FileSystemStorage

# Coding Dojo project - Holiday Greetings

# Create your views here.

def home(request):
    return render(request, "home.html")

def success(request):
    if 'user_id' not in request.session:
        return redirect("/")
    return render(request, "success.html")
def create_card(user):
    # create a card object, populate with defaults
    d_title = "Type your title here"
    d_text = "Type your greeting text here"
    d_image = "xmas1.jpg"

    a_card = Card.objects.create(title=d_title, text=d_text, img_name=d_image, user=user)
    print(f"Card id: {a_card.id}")
    return a_card

def register(request):
    if request.method=="POST":
        errors = User.objects.validate(request.POST)
        if errors:
            for error in errors:
                messages.error(request, errors[error])
            return redirect('/')

        # password encrypt
        user_pw = request.POST['pw']
        hash_pw = bcrypt.hashpw(user_pw.encode(), bcrypt.gensalt()).decode()

        # create the new user
        new_user = User.objects.create(first_name=request.POST['f_n'], last_name=request.POST['l_n'], email=request.POST['email'], password=hash_pw)

        # store info in session
        request.session['user_id'] = new_user.id
        request.session['user_name'] = f"{new_user.first_name} {new_user.last_name}"

        # create the users Card, redirect to make a card page
        a_card = create_card(new_user)
        request.session['card_id'] = a_card.id
        return redirect('/make_card')
    
    # wasn't a post request, send 'em back
    return redirect('/')

def login(request):
    if request.method == 'POST':
        # see if email is in the DB
        logged_user = User.objects.filter(email=request.POST['email'])
        if logged_user:
            logged_user = logged_user[0]    # strip the curlies 
            # compare the passwords
            if bcrypt.checkpw(request.POST['pw'].encode(), logged_user.password.encode()):
                request.session['user_id'] = logged_user.id
                request.session['user_name'] = f"{logged_user.first_name} {logged_user.last_name}"

                # create the users Card, redirect to make a card page
                a_card = create_card(logged_user)
                request.session['card_id'] = a_card.id
                return redirect('/make_card')

    # if we get here, not a user, or wrong password
    # TODO: put an error message in errors
    return redirect('/')

def sendmail(request):
    if request.method == "POST":
        recipient = request.POST['email_addr']
        print(f"About to send email, recipient: {recipient}")
        send_mail(
            'Holiday Greeting',
            'You are invited to view a holiday greeting...',
            'beswetherickmark@gmail.com',
            [recipient],
        fail_silently=False,
    )
    return redirect('/make_card')

def upload(request):
    print("Made it to upload")
    if request.method == "POST":
        # uploaded file name and contents in FILES dict
        # must set enctype="multipart/form-data" in <form> tag
        print("request.FILES:", request.FILES)
        up_file = request.FILES['myfile']
        # save uploaded file to local file system, goes to MEDIA_ROOT
        fs = FileSystemStorage()
        filename = fs.save(up_file.name, up_file)
        # make relative URL that serves image
        uf_url = fs.url(filename)
        print (f"In upload, url: {uf_url}")
        # TODO: pass URL to html file thru context(?)
    return redirect('/show_img')

def make_card(request):
    card_id = request.session['card_id']
    card = Card.objects.get(id=card_id)
    print(f"In make_card, card_id: {card_id}, card image: {card.img_name}")
    request.session['card_title'] = card.title
    request.session['card_text'] = card.text
    request.session['card_image'] = card.img_name
    return render(request, "make_card.html")

def update_text(request, card_id):
    if request.method == "POST":
        card = Card.objects.get(id=card_id)
        # change the text greeting
        card.text = request.POST['hg_text']
        card.save()
        return redirect("/make_card")

    # not a post request, send em back to login page
    return redirect('/')

def update_image(request, card_id):
    if request.method == "POST":
        up_file = request.FILES['myfile']
        # save uploaded file to local file system, goes to MEDIA_ROOT
        fs = FileSystemStorage()
        filename = fs.save(up_file.name, up_file)
        print(f"up_file: {up_file}, filename: {filename}")
        card = Card.objects.get(id=card_id)
        card.img_name = up_file.name
        card.save()
        return redirect("/make_card")

    # not a post request, send em back to login page
    return redirect('/')
