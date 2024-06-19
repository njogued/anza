from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.urls import reverse
from .models import Business
from .forms import CreateBusinessForm, BusinessUpdateForm
from django.urls import reverse_lazy

# Create your views here.
class CreateBusinessView(LoginRequiredMixin, CreateView):
    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})
    def post(self, request):
        curr_user = request.user
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            business = form.save(commit=False)
            business.owner = curr_user
            business.save()
            success_url = reverse('detail_business', kwargs={'business_id': business.business_id})
            return redirect(success_url)
        return render(request, self.template_name, {"form": form})
    model = Business
    form_class = CreateBusinessForm
    success_url = reverse_lazy("home")
    template_name = "create_business.html"
    login_url = "/users/login"

class BusinessDetailView(DetailView):
    model = Business
    template_name = "detail_business.html"
    context_object_name = "business"
    pk_url_kwarg = 'business_id'

class BusinessListView(ListView):
    model = Business
    template_name = "list_business.html"
    context_object_name = "businesses"
    # paginate_by = 10
    # ordering = ['name'] 

class BusinessUpdateView(UpdateView):
    model = Business
    form_class = BusinessUpdateForm
    template_name = "update_business.html"
    context_object_name = 'business'
    pk_url_kwarg = 'business_id'

    def get_success_url(self):
        return reverse_lazy('detail_business', kwargs={'business_id': self.object.business_id})
    
    def form_valid(self, form):
        curr_user = self.request.user
        business = form.save(commit=False)
        business.owner = curr_user
        business.save()
        return redirect(self.get_success_url())


class BusinessDeleteView(DeleteView):
    model = Business
    template_name = "delete_business.html"
    success_url = reverse_lazy("home")
    pk_url_kwarg = 'business_id'
