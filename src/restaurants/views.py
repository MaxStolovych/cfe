from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView

from .models import Restaurant
from .forms import RestaurantCreateForm, RestaurantLocationCreateForm

# Create your views here.


class RestaurantListView(LoginRequiredMixin, ListView):
    def get_queryset(self):
       return Restaurant.objects.filter(owner=self.request.user)
 

class RestaurantDetailView(LoginRequiredMixin, DetailView):
    def get_queryset(self):
        return Restaurant.objects.filter(owner=self.request.user)


#    def get_object(self, *args, **kwargs):
#        rest_id = self.kwargs.get('rest_id')
#        obj = get_object_or_404(Restaurant, id=rest_id)
#        return obj
        

class RestaurantCreateView(LoginRequiredMixin, CreateView):
    form_class = RestaurantLocationCreateForm
    template_name = 'form.html'
    #success_url = "/restaurants/"

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.owner = self.request.user
        instance.save()
        return super(RestaurantCreateView, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(RestaurantCreateView, self).get_context_data(*args, **kwargs)
        context['title'] = "Add Restaurant"
        return context

class RestaurantUpdateView(LoginRequiredMixin, UpdateView):
    form_class = RestaurantLocationCreateForm
    template_name = 'restaurants/detail-update.html'
    #success_url = "/restaurants/"

    def get_context_data(self, *args, **kwargs):
        context = super(RestaurantUpdateView, self).get_context_data(*args, **kwargs)
        name = self.get_object().name
        context['title'] = "Update Restaurant: {}".format(name)
        return context

    def get_queryset(self):
        return Restaurant.objects.filter(owner=self.request.user)
