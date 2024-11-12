from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import models

from home.models import Contents, Category, Comment
from home.forms import CreatePostForm

@login_required
def dashboard(request):
    current_user =request.user
    data = Contents.objects.filter(user=current_user)
    t_post = data.count()
    t_like = 0
    t_view = 0
    t_dislik = 0
    t_comment = 0
    for post in data:
        t_like += post.likes
        t_view += post.views
        t_dislik += post.dislikes
        t_comment += Comment.objects.filter(content=post, content__user = current_user).count()

    
    context = {
        "posts":t_post,
        "likes":t_like,
        "views":t_view,
        "dislikes":t_dislik,
        "comments":t_comment,
        "most_viewed":data.order_by("-views"),
    }

    
    return render(request, "admin/dashboard.html", context )



@login_required
def dashboard_options(request, page):
    if page =="create":
        if request.method == 'POST':
            form = CreatePostForm(request.POST, request.FILES)
            if form.is_valid():
                post = form.save(commit=False)
                category_name = request.POST.get('category')
                if category_name is None or category_name == '':
                    default_category = get_object_or_404(Category, name='Others')
                    post.category = default_category
            
                post.user = request.user
                
                post.save()
                messages.success(request, "Congrats! Your post has been uploaded successfully.")
                return redirect('dashboard')
        else:
            form = CreatePostForm()

        context ={
            "form":form,
        }   
        return render(request, "admin/create_post.html", context)
    
    elif page =="read":

        data = Contents.objects.filter(user=request.user, )
        context={
            "data":data,
        }
        return render(request, "admin/read_post.html", context)
        
    else:
        return render(request, "home/404.html")
    
    
@login_required
def update_post(request, uid):
    post = get_object_or_404(Contents, pk=uid)

    if request.method=="POST":
        form = CreatePostForm(request.POST,request.FILES,instance=post )
        if form.is_valid():
            form.save()
            messages.success(request, "Your post has been updated!")
            return redirect(request.path)
    else:
        form = CreatePostForm(instance=post)

    context = {
        "form":form,
    }
    return render(request, "admin/update_post.html", context)

@login_required
def delete_post(request, uid):
    try:
        post = get_object_or_404(Contents, pk=uid)
        if post.user == request.user:
            post.delete()
            messages.warning(request,"This post permanently deleted!")
            return redirect("option", page="read")
        else:
            messages.error(request,"You are not permitted to delete this post! Fall back.")
            return redirect(request.path)
    except Exception as e:
        messages.info(request, f"{e}")
        return redirect(request.path)


'''
# ===================== ++++++++++ DASHBOARD ++++++++++ =================
# DONE 
@login_required
def the_dashb(request):
    def viewer_in_format(num):
        magnitudes = ['', 'K', 'M', 'G', 'T', 'P']
        mag = 0
        if num < 1000:
            return str(num)
        while num >= 1000:
            mag += 1
            num /= 1000
        return f"{num}{magnitudes[mag]}"

# FORMAT ALL NUMBERS IN 1k, 1M, 1B etc -->
   
    t_p = Contents.objects.filter(user=request.user).count()
    t_l = Contents.objects.filter(user=request.user).aggregate(total_likes=models.Sum('likes'))['total_likes'] or 0
    t_t = Contents.objects.filter(user=request.user).aggregate(total_views=models.Sum('views'))['total_views'] or 0
    t_dl = Contents.objects.filter(user=request.user).aggregate(total_views=models.Sum('dislikes'))['total_views'] or 0


    t_pst = viewer_in_format(t_p)
    ttl_likes = viewer_in_format(t_l)
    t_v = viewer_in_format(t_t)
    
    # print(f'answer  {viewer_in_format(t_v)}') 
    # t_v = Contents.objects.all()
    # print(t_p)

    profile_data = {
    'user': request.user,
    'profile_picture': request.user.userprofile.profile_picture.url,
    'bio_data': request.user.userprofile.bio_data,
    # ---------------------
    'ttl_pst' : t_pst,
    't_lk' : ttl_likes,
    't_v' : t_v,
    'ttl_dslk' : t_dl,
    
    }
    return render(request, 'dashboard.html', {'profile' : profile_data})


# DONE

@login_required
def make_post(request):
    previous_page = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form = CreatePostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            category_name = request.POST.get('category')
            if category_name is None or category_name == '':
                default_category = get_object_or_404(Category, name='Others')
                post.category = default_category
           
            post.user = request.user
            
            post.save()
            messages.success(request, "Congrats! Your post has been uploaded successfully.")
            return redirect('the_dashb')
    else:
        form = CreatePostForm()
    return render(request, 'make_post.html', {'form': form, 'previous_page': previous_page})



# DONE
@login_required
def your_posts(request):
    
    user_posts = Contents.objects.filter(user=request.user)
    # descr = Contents.objects.values_list('descript', flat=True)

    # print(descr)
    content = {
        'user_posts': user_posts,
        'profile': {
            'user': request.user,
            'profile_picture': request.user.userprofile.profile_picture.url,
            'bio_data': request.user.userprofile.bio_data,
            }
            # ---------------------

    }

    return render(request, 'your_posts.html', context=content)

# DONE
@login_required
def your_profile(request):

    profile = request.user.userprofile
    
    if request.method == "POST":

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        bio_data = request.POST.get('bio_data')
        profile_picture = request.FILES.get('profile_picture')  # Get the uploaded file
        if profile_picture:
            profile.profile_picture = profile_picture
            profile.save()
        # Update user profile data
        request.user.first_name = first_name
        request.user.last_name = last_name
        profile.bio_data = bio_data
        request.user.save()
        profile.save()


    profile_data = {
        'user': request.user,
        'profile_picture': profile.profile_picture.url,
        'bio_data': profile.bio_data,
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
    }

    context = {
        'profile': profile_data,
        
    }

    return render(request, 'your_profile.html', context)

# DONE
@login_required
def change_password(request):

    previous_page = request.META.get('HTTP_REFERER')
    
    if request.method == 'POST':
        form = EditedPassChangeForm(user = request.user, data = request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, "your password has been successfully changed ! ".title())
    else:
        form = EditedPassChangeForm(request.user)

    alllll = {'form' : form, 
              'previous_page': previous_page,
              'profile': {'user': request.user,
                          'profile_picture': request.user.userprofile.profile_picture.url,
                          'bio_data': request.user.userprofile.bio_data,
                            # ---------------------
                            
                          }
            }

    
    return render(request, 'change_password.html' , context=alllll )


# DONE
@login_required
def edit_post(request, key):
    content = Contents.objects.get(slug=key)

    if request.method == 'POST':
        form = CreatePostForm(request.POST, request.FILES, instance=content)
        if form.is_valid():
            form.save()
            messages.success(request, "Your chnages has been updated !")
            return redirect('the_dashb')
    else:
        form = CreatePostForm(instance=content)

    return render(request, 'edit.html', {'form': form, 'current_picture': content.picture})


# DONE
@login_required
def delete_post(request, slug):
    post = get_object_or_404(Contents, slug=slug, user=request.user)
    if request.method == 'POST':
        post.delete()
        return redirect('your_posts')
    else:
        # Handle GET request if needed
        pass


# DONE
def feedback(request):
    if request.method == "POST":
        your_data = SayToMe(
            name_is=request.POST.get('name_is'),
            saying=request.POST.get('saying')
        )
        messages.success(request, "Your feedback or your message has reached us. Thank you.")
        your_data.save()
        return redirect('homes')
    return render(request, 'about.html')



def dynamic_option(request, option):
    
    if option == 'make_post':
        return make_post(request)
    elif option == 'your_posts':
        return your_posts(request)
    elif option == 'your_profile':
        return your_profile(request)
    elif option == 'change_password':
        return change_password(request)
    else:
        return render(request, 'index.html')  # Handle invalid options



'''
