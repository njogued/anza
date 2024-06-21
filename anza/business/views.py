from django.urls import reverse
from django.views import View
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.http import HttpResponseForbidden, HttpResponse, HttpResponseRedirect
from .models import Business
from .forms import CreateBusinessForm, BusinessUpdateForm

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
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.archived:
            obj = None
        return obj
    
    def get_context_data(self, **kwargs):
        # Get the existing context data from the parent class
        context = super().get_context_data(**kwargs)
        # If the business object is None, add a flag to the context
        if self.object is None:
            context['business_deleted'] = True
        else:
            context['business_deleted'] = False
        return context
    
    def render_to_response(self, context, **response_kwargs):
        # Check the flag in the context to see if the business is deleted
        if context.get('business_deleted'):
            return HttpResponse("Business deleted")
        # If not archived, call the parent class's render_to_response method
        return super().render_to_response(context, **response_kwargs)

class BusinessListView(ListView):
    model = Business
    template_name = "list_business.html"
    context_object_name = "businesses"
    # paginate_by = 10
    # ordering = ['name']
    def get_queryset(self):
        return Business.objects.filter(archived=False)

class BusinessUpdateView(UpdateView):
    model = Business
    form_class = BusinessUpdateForm
    template_name = "update_business.html"
    context_object_name = 'business'
    pk_url_kwarg = 'business_id'

    def get_success_url(self):
        return reverse_lazy('detail_business', kwargs={'business_id': self.object.business_id})
    
    def dispatch(self, request, *args, **kwargs):
        business = self.get_object()
        if business.owner != self.request.user:
            return HttpResponseForbidden("You are not allowed to update business")
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        curr_user = self.request.user
        business = form.save(commit=False)
        business.owner = curr_user
        business.save()
        return redirect(self.get_success_url())


class BusinessDeleteView(View):
    template_name = "delete_business.html"
    success_url = reverse_lazy("home")
    pk_url_kwarg = 'business_id'
    
    def dispatch(self, request, *args, **kwargs):
        business_id = kwargs.get(self.pk_url_kwarg)
        business = get_object_or_404(Business, pk=business_id)
        if business.owner != request.user:
            return HttpResponseForbidden("You are not allowed to delete this business")
        self.business = business
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'business': self.business})

    def post(self, request, *args, **kwargs):
        business_id = kwargs.get(self.pk_url_kwarg)
        business = get_object_or_404(Business, pk=business_id)
        business.archived = True
        business.save()
        return redirect(self.success_url)