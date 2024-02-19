from django.utils.text import slugify
import random, string

def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def unique_slug_generator(instance,new_slug=None):
    '''This is for a Django project and it assumes your instance has a model with a slug field and a title character (char) field.'''
    if new_slug is not None:
        slug = new_slug
    elif instance.user_profile is not None and instance.property_city is not None and instance.property_state is not None and instance.property_area is None:
        slug = slugify(instance.user_profile.first_name + "-" + instance.user_profile.last_name + "-" + instance.property_city.city_name + "-" + instance.property_state.state_name + "-" + str(instance.id)+instance.property_state.state_name)
    elif instance.user_profile is not None and instance.property_city is not None and instance.property_state is not None and instance.property_area is not None:
        slug = slugify(instance.user_profile.first_name + "-" + instance.user_profile.last_name + "-" + instance.property_area.area_name + "-" + instance.property_city.city_name + "-" + instance.property_state.state_name + "-" + str(instance.id)+instance.property_state.state_name)
    
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
            slug=slug,
            randstr=random_string_generator(size=5)
        )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug

# def unique_slug_generator(instance, new_slug=None):
#     """
#     This is for a Django project and it assumes your instance 
#     has a model with a slug field and a title character (char) field.
#     """

#     if new_slug is not None:
#         slug = new_slug
#     elif instance.property_area is None and instance.property_city is None and instance.property_state is None:
#         slug = slugify(instance.property_title +"-"+ instance.property_address_1)
#     elif instance.property_area is None and instance.property_city is not None and instance.property_state is not None:
#         slug = slugify(instance.property_title +"-"+ instance.property_address_1 +"-"+ instance.property_city.city_name +"-"+ instance.property_state.state_name +"-"+ instance.property_zip)
#     else:
#         slug = slugify(instance.property_title +"-"+ instance.property_address_1 +"-"+ instance.property_area.area_name +"-"+ instance.property_city.city_name +"-"+ instance.property_state.state_name +"-"+ instance.property_zip)

#     if instance.property_listing_type.property_listing_name == "Residential":
#         if instance.propertylisting_type.listing_type == "Rental":
#             slug = slugify(slug +"-"+ instance.property_listing_type.property_listing_name +"-"+ instance.propertylisting_type.listing_type +"-"+ instance.property_main_category.Main_category +"-price="+str(instance.property_listing_amount) +"-Bedrooms="+str(instance.Bedrooms))
#         elif instance.propertylisting_type.listing_type == "Sales":
#             slug = slugify(slug +"-"+ instance.property_listing_type.property_listing_name +"-"+ instance.propertylisting_type.listing_type +"-"+ instance.property_main_category.Main_category +"-price="+str(instance.property_listing_amount) +"-Bedrooms="+str(instance.Bedrooms))
#     elif instance.property_listing_type.property_listing_name == "Commercial":
#         if instance.propertylisting_type.listing_type == "Commercial Leasing":
#             slug = slugify(slug +"-"+ instance.property_listing_type.property_listing_name +"-"+ instance.propertylisting_type.listing_type +"-"+ instance.property_main_category.Main_category +"-price="+str(instance.property_listing_amount) +"-Units="+ str(instance.Units))
#         elif instance.propertylisting_type.listing_type == "Commercial Sales":
#             slug = slugify(slug +"-"+ instance.property_listing_type.property_listing_name +"-"+ instance.propertylisting_type.listing_type +"-"+ instance.property_main_category.Main_category +"-price="+str(instance.property_listing_amount) +"-Units="+ str(instance.Units))


#     Klass = instance.__class__
#     qs_exists = Klass.objects.filter(slug=slug).exists()
#     if qs_exists:
#         new_slug = "{slug}-{randstr}".format(
#             slug=slug,
#             randstr=random_string_generator(size=5)
#         )
#         return unique_slug_generator(instance, new_slug=new_slug)
#     return slug
