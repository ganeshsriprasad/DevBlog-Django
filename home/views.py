from django.http import  HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import RegistrationForm , EditedPassChangeForm,CreatePostForm,CommentForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,logout , update_session_auth_hash, authenticate
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404 
from .models import Contents, Comment, MsgFromAdmin, SayToMe, UserProfile, Category
from django.db.utils import IntegrityError
from django.db import models
from django.utils.html import strip_tags

def home(request):
    category = request.GET.get('category')
    search_query = request.GET.get('searchpost')

    if category:
        all_post = Contents.objects.filter(category__name=category).order_by('-uploaded_at')
        

    elif search_query:
        all_post = Contents.objects.filter(title__icontains=search_query).order_by('-uploaded_at')
    else:
        
        all_post = Contents.objects.all().order_by('-uploaded_at')

    if request.method == 'GET':
        posttitle = request.GET.get('searchpost')
        if posttitle != None :
            all_post = Contents.objects.filter(title__icontains = posttitle)
        elif posttitle =='' or posttitle=='#':
            all_post = Contents.objects.all().order_by('-uploaded_at')

    # filter_nm_exmpl = list(Contents.objects.values_list('title', flat=True))


    # ----- Available Category Name -----------
    cat = list(set(Contents.objects.values_list('category__name', flat=True)))
    # print(cat)
    
    # ---------- x -----------


    #------ LOGIC FOR FILTER OUT THE POPULER POSTS OF EACH CATEGORY ------
   
    top_posts = []
    
    for category in cat:
        top_post = Contents.objects.filter(category__name=category).order_by('-views')
        top_post1 = top_post.first()

        try:
            top_post2 = top_post[1]
        except:
            top_post2=None

        top_posts.append(top_post1)
        if top_post2:
            top_posts.append(top_post2)
    
    
    # print(top_posts)

    # ------------------------------  X ---------------------------------

    for post in top_posts:
        post.total_comments = Comment.objects.filter(content=post).count()

        # ---------LOGIC To see get the PURE description and calculate time ----------
        descript_text = strip_tags(post.descript)
        lenis = descript_text.replace(' ', '')
        # print(lenis)
        to_read = str((len(lenis) * (15/100)/60)).split('.')
        timeneeds = (f"{to_read[0]}.{(to_read[1])[:1]} min")
        
        
        # (*** THIS WAY ANOTHER MODELS VALUE OR OWN MODEL VALUE CAN CALCULATE AND NEWLY PASS TO EACH POSTS . IMP***)
        
        post.read_time = timeneeds

    for post in all_post:
        post.total_comments = Comment.objects.filter(content=post).count()

    paginator = Paginator(all_post, 20)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    e_d = {}
    for item in cat:
        count = Contents.objects.filter(category__name=item).order_by('-uploaded_at').count()
        e_d[item] = count

    # -- checking if dictiory print perfect or not --
    # for item, count in e_d.items():
    #     print(item, count)

    try:
        mymsg = list(MsgFromAdmin.objects.all()[:2])
    except:
        mymsg = []

    recent_comment = Comment.objects.all().order_by("created_at")[:7]
    home_content = {
        "5_recent":all_post[:5],
        "page_obj": page_obj,
        "categories": e_d,
        "top_posts": top_posts,
        "headlinetoday": mymsg[0] if mymsg else None,
        "msgtwo": mymsg[1] if len(mymsg) > 1 else None,
        "recent_comment":recent_comment,
    }


    
    return render(request, "home/index.html", context=home_content  )

# WORK REMAIN -- Like, Dislike 
def artical_view(request, the_artical):

    content = get_object_or_404(Contents, slug=the_artical)
    user_profile = content.user.profile

    # Logic for read time
    descript_text = strip_tags(content.descript)
    lenis = descript_text.replace(' ', '')
    to_read = str((len(lenis) * (15 / 100) / 60)).split('.')
    timeneed = (f"{to_read[0]}.{(to_read[1])[:1]} min")

    # The most viewed post
    most_viewed_post = Contents.objects.all().order_by('-views')[:6]
    # Comments for the content
    comments = Comment.objects.filter(content=content)

    # Handle comment form submission
    if request.method == "POST":
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            the_form = form.save(commit=False)
            the_form.content = content
            the_form.save()
            return redirect(request.path)
    else:
        form = CommentForm()


    # Check if the article has been viewed in this session
    has_viewed = request.session.get(f'viewed_article_{content.pk}', False)
    if not has_viewed:
        content.views += 1
        content.save()
        request.session[f'viewed_article_{content.pk}'] = True

    # Context for rendering the template
    context = {
        'categories': Category.objects.all(),
        'content': content,
        'posts': most_viewed_post,
        'user_profile': user_profile,
        'all_comment': comments,
        'read': timeneed,
        'form': form,
    }

    return render(request, 'home/artical.html', context)

def all_posts(request):
    category = request.GET.get('category')
    search_query = request.GET.get('searchpost')

    if category:
        all_post = Contents.objects.filter(category__name=category).order_by('-uploaded_at')
        

    elif search_query:
        all_post = Contents.objects.filter(title__icontains=search_query).order_by('-uploaded_at')
    else:
        
        all_post = Contents.objects.all().order_by('-uploaded_at')
    

    paginator = Paginator(all_post, 20)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)


    categories = Category.objects.all()
    context = {
        "page_obj":page_obj,
        "categories":categories,
        "top_5": None,
    }
    return render(request, "home/posts.html", context )


# ================ ++++++++ AUTHORIZATION +++++++++ ==================

# DONE
def Registration(request):
    if request.user.is_authenticated:
        return redirect('homes')
    else:
        if request.method == 'POST':
            reg_form = RegistrationForm(request.POST)
            if reg_form.is_valid():
                try:
                    # Save the user
                    user = reg_form.save()

                    # Create a UserProfile for the user
                    # user_profile = UserProfile(user=user)
                    
                    # user_profile.save()

                    messages.success(request, "Congrats! Your account was created successfully.")
                    return redirect('the_login')

                except IntegrityError:
                    messages.error(request, "Username already exists. Please choose a different username.")
                    return redirect('the_signup')

        else:
            reg_form = RegistrationForm()

        context = {'form': reg_form}
        return render(request, 'auth/registation.html', context)

# DONE
def the_login(request):
    if request.user.is_authenticated:
        messages.success(request, "You are already logged in.")
        return redirect('homes')

    if request.method == 'POST':
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, "You have successfully logged in.")
                print("LOGIN DONE")
                return redirect('homes')  # Redirect to a success page, e.g., home
            else:
                messages.error(request, "Invalid username or password.")   
                print("Invalid")         

        '''BELOW ONE ALSO WORK AND THIS IS IN-BUILT'''

        # the_form = AuthenticationForm(request=request, data=request.POST)
        # if the_form.is_valid():
        #     user = the_form.get_user()
        #     login(request, user)
        #     messages.success(request, f"Hey {user.username}! Welcome to the BlogVerse. You can now manage your posts.")
        #     return redirect("homes")
        # else:
        #     messages.error(request, "Invalid username or password")
        #     return redirect('the_login')
    # else:
    #     the_form = AuthenticationForm()

    return render(request, 'auth/login.html') 

# Done
@login_required
def the_logout(request):
    logout(request)
    
    messages.warning(request, "You have successfully logged out! and you have no longer access to perform any operation")

    return redirect('homes')


# Below all are temprory for checking purpose

def temp(request):
    return render(request, "temp.html")


def about(request):
    return render(request,"home/aboutme.html")

def contact(request):
    return render(request,"home/contactme.html")

