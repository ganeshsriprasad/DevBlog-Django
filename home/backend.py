from django.utils.text import slugify
import random
import string

# 1. Genarate a random string and presurve for later
# 2. If new slug match with existing slug then add that random string with the slug and return new_slug

def custom_slugify(the_title):
    
    random_string = ''.join(random.choices(string.ascii_letters, k=5))
    new_chked_title = slugify(f"{the_title}-{random_string}")
   
    from home.models import Contents
    if Contents.objects.filter(slug=new_chked_title).first():
        random_string = ''.join(random.choices(string.ascii_letters, k=5))
        new_chked_title = f"{new_chked_title}-{random_string}"
        return new_chked_title

    return new_chked_title


