from django.conf import settings
from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save, post_save
from django.core.urlresolvers import reverse

from .utils import unique_slug_generator
from .validators import validate_category

User = settings.AUTH_USER_MODEL

class RestaurantQuerySet(models.query.QuerySet):
    def search(self, query): #Restaurant.objects.all().search(query) #Restaurant.objects.filter(something).search()
        if query:
            query = query.strip()
            return self.filter(
                Q(name__icontains=query) |
                Q(location__icontains=query) |
                Q(category__icontains=query) |
                Q(item__name__icontains=query) |
                Q(item__contents__icontains=query)
                ).distinct()

class RestaurantManager(models.Manager):
    def get_queryset(self):
        return RestaurantQuerySet(self.model, using=self._db)

    def search(self, query): #Restaurant.objects.search()
        return self.get_queryset().filter(name__icontains=query)

class Restaurant(models.Model):
    owner      = models.ForeignKey(User)
    name       = models.CharField(max_length=120)
    location   = models.CharField(max_length=120, null=True, blank=True) 
    category   = models.CharField(max_length=120, null=True, blank=True,
                                  validators=[validate_category])
    timestamp  = models.DateTimeField(auto_now_add=True)
    updated    = models.DateTimeField(auto_now=True)
    slug       = models.SlugField(null=True, blank=True)

    objects = RestaurantManager()

    def __str__(self):
        return self.name

    # Returns success page when model is created
    # with viewname param via reverse func.
    def get_absolute_url(self):
        # return '/restaurants/{}'.format(self.slug)
        return reverse('restaurants:detail', kwargs={'slug': self.slug})

    # Allows to use title on Restaurant objects
    @property
    def title(self):
        return self.name
    

def r_pre_save_receiver(sender, instance, *args, **kwargs):
    instance.category = instance.category.capitalize()
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
        
#def r_post_save_receiver(sender, instance, created, *args, **kwargs):
#    print('saved')
#    print(instance.timestamp)
#    if not instance.slug:
#        instance.slug = unique_slug_generator(instance)
#        instance.save()
        
pre_save.connect(r_pre_save_receiver, sender=Restaurant)

# post_save.connect(r_post_save_receiver, sender=RestaurantLocation)