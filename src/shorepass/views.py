from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User
from datetime import datetime
from django.urls import reverse_lazy
from django.views.generic import DetailView,CreateView,UpdateView,DeleteView,ListView
from django.db.models import Q,F
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib.auth.decorators import permission_required
# @permission_required('polls.add_choice', login_url='/loginpage/')
from django.contrib.auth.mixins import PermissionRequiredMixin
# permission_required = 'polls.add_choice'
# # Or multiple of permissions:
# permission_required = ('polls.view_choice', 'polls.change_choice')
from django.core.exceptions import PermissionDenied


from .models import Shore

class ShoreListView(LoginRequiredMixin,ListView):
    model = Shore
    paginate_by = 50

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query :
            if self.request.user.has_perm('shorepass.verify_shore') or  self.request.user.has_perm('shorepass.execute_job') :
                # For Staff or Admin
                # Modify on Nov 20,2020 -- To support search by User name
                return Shore.objects.filter(Q(booking__icontains=query)|
                                        Q(user__username=query)).order_by('-updated')
                                        #Q(booking__name__icontains=query)| -->Removed for optimize
            else:
                return Shore.objects.filter(Q(booking__icontains=query) ,
                                        user__username=self.request.user ).order_by('-updated')
                                        # Q(booking__name__icontains=query) ,-->Removed for optimize
        
        if self.request.user.has_perm('shorepass.verify_shore') or  self.request.user.has_perm('shorepass.execute_job') :
            return Shore.objects.all().order_by('-updated')[:200]

        return Shore.objects.filter(user__username=self.request.user).order_by('-updated')[:200]
    
    def get_context_data(self,**kwargs):
        context = super(ShoreListView,self).get_context_data(**kwargs)
        # context['addresses'] = Address.objects.filter(user__username=self.request.user)
        return context

class ShoreDetailView(LoginRequiredMixin,DetailView):
    model = Shore
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        user_obj = self.request.user
        if user_obj.is_staff or user_obj.is_superuser :
            return super().dispatch(request,*args,**kwargs)

        if not obj.user == self.request.user :
            raise PermissionDenied
        return super().dispatch(request,*args,**kwargs)


class ShoreCreateView(LoginRequiredMixin,CreateView):
    model = Shore
    fields = ['booking','vessel_name','pod','voy',
            'terminal','agent','customer','shorefile1','shorefile2','containers_json']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # shorepass_base_url 			= f"{reverse_lazy('shorepass:list')}address/"
        context['shorepass_api_url'] 		= '/api/shorepass/'
        return context
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ShoreCreateView, self).form_valid(form)


# For attached file
class ShoreUpdateFile1(LoginRequiredMixin,UpdateView):
    model = Shore
    fields = ['shorefile1']
    template_name_suffix = '_update_shorefile_form'
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        user_obj = self.request.user
        if user_obj.is_staff or user_obj.is_superuser :
            return super().dispatch(request,*args,**kwargs)
            
        if not obj.user == self.request.user :
            raise PermissionDenied
        return super().dispatch(request,*args,**kwargs)

class ShoreUpdateFile2(LoginRequiredMixin,UpdateView):
    model = Shore
    fields = ['shorefile2']
    template_name_suffix = '_update_shorefile_form'
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        user_obj = self.request.user
        if user_obj.is_staff or user_obj.is_superuser :
            return super().dispatch(request,*args,**kwargs)
            
        if not obj.user == self.request.user :
            raise PermissionDenied
        return super().dispatch(request,*args,**kwargs)

class ShoreDeleteView(LoginRequiredMixin,DeleteView):
    model = Shore
    success_url = reverse_lazy('shorepass:list')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        user_obj = self.request.user
        if user_obj.is_staff or user_obj.is_superuser :
            return super().dispatch(request,*args,**kwargs)
            
        if not obj.user == self.request.user :
            raise PermissionDenied
        return super().dispatch(request,*args,**kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if (self.object.user == request.user) or request.user.is_superuser or request.user.is_staff :
            self.object.delete()
            return redirect(self.get_success_url())
        else:
            raise Http404("Not allow to delete") #or return HttpResponse('404_url')

class ShoreUpdateExecuteJob(PermissionRequiredMixin,LoginRequiredMixin,UpdateView):
    model = Shore
    fields = ['execute_job']
    template_name_suffix = '_update_executejob_form'
    permission_required = ('shorepass.verify_shore', 'shorepass.execute_job')

    def form_valid(self, form):
        import datetime, pytz
        tz = pytz.timezone('Asia/Bangkok')
        form.instance.execute_date = datetime.datetime.now(tz=tz)#datetime.now()
        # Added on Oct 29,2020 -- To save executor
        form.instance.execute_by = self.request.user
        return super(ShoreUpdateExecuteJob, self).form_valid(form)

class ShoreUpdateContactMessage(PermissionRequiredMixin,LoginRequiredMixin,UpdateView):
    model = Shore
    fields = ['need_contact','message']
    template_name_suffix = '_update_message_form'
    permission_required = ('shorepass.verify_shore', 'shorepass.execute_job')