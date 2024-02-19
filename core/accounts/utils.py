from django.core.mail import EmailMessage


import threading


class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        # print("yes")
        self.email.send()


class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'], body=data['email_body'], to=[data['to_email']])
        # print(email)
        EmailThread(email).start()


import random
import string

from django.utils.text import slugify


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


# def unique_slug_generator(instance, new_slug=None):
#     """
#     This is for a Django project and it assumes your instance 
#     has a model with a slug field and a title character (char) field.
#     """
    
#     if new_slug is not None:
#         slug = new_slug
#     elif instance.unique_id is None:
#         slug = slugify(instance.first_name +"-"+ instance.last_name)
#     elif instance.citymaster is None or instance.state is None:
#         slug = slugify(instance.first_name +"-"+ instance.last_name +"-"+ instance.unique_id)
#     else:
#         slug = slugify(instance.first_name +"-"+ instance.last_name +"-"+ instance.unique_id +"-"+ instance.citymaster.city_name +"-"+ instance.state.state_name)

#     Klass = instance.__class__
#     qs_exists = Klass.objects.filter(slug=slug).exists()
#     if qs_exists:
#         new_slug = "{slug}-{randstr}".format(
#             slug=slug,
#             randstr=random_string_generator(size=5)
#         )
#         return unique_slug_generator(instance, new_slug=new_slug)
#     return slug

def unique_slug_generator(instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(str(instance.user_type.user.id) +"-"+ instance.first_name +"-"+ instance.last_name)
    
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
            slug=slug,
            randstr=random_string_generator(size=5) 
        )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug