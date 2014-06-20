from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from django.contrib.messages import info, error
from .models import IppcUserProfile, PestStatus,Files, PestReport, IS_PUBLIC, IS_HIDDEN, Publication, BasicReporting, BASIC_REP_TYPE_CHOICES, EventReporting, EVT_REP_TYPE_CHOICES,PestFreeArea,ImplementationISPM,CountryPage,REGIONS
from mezzanine.core.models import Displayable, CONTENT_STATUS_DRAFT, CONTENT_STATUS_PUBLISHED
from .forms import PestReportForm, FilesForm, BasicReportingForm, EventReportingForm, PestFreeAreaForm,ImplementationISPMForm

from django.views.generic import ListView, MonthArchiveView, YearArchiveView, DetailView, TemplateView, CreateView
from django.core.urlresolvers import reverse

from django.template.defaultfilters import slugify, lower
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, redirect

from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator

def get_profile():
    return IppcUserProfile.objects.all()

# def pest_report_country():
#     return PestReport.objects.all()
    
class CountryView(TemplateView):
    """ 
    Individual country homepage 
    """
    template_name = 'countries/country_page.html'
    
    def get_context_data(self, **kwargs): # http://stackoverflow.com/a/15515220
        context = super(TemplateView, self).get_context_data(**kwargs)
        context['event_types'] =EVT_REP_TYPE_CHOICES
        context['basic_types'] =BASIC_REP_TYPE_CHOICES 
        context.update({
            'country': self.kwargs['country']
            # 'editors': self.kwargs['editors']
            # 'profile_user': self.kwargs['profile_user']
        })
        return context


class PestReportListView(ListView):
    """
    Pest reports
        http://stackoverflow.com/questions/8547880/listing-object-with-specific-tag-using-django-taggit
        http://stackoverflow.com/a/7382708/412329
    """
    context_object_name = 'latest'
    model = PestReport
    date_field = 'publish_date'
    template_name = 'countries/pest_report_list.html'
    queryset = PestReport.objects.all().order_by('-publish_date', 'title')
    allow_future = False
    allow_empty = True
    paginate_by = 30

    def get_queryset(self):
        """ only return pest reports from the specific country """
        # self.country = get_object_or_404(CountryPage, country=self.kwargs['country'])
        self.country = self.kwargs['country']
        # CountryPage country_slug == country URL parameter keyword argument
        return PestReport.objects.filter(country__country_slug=self.country, status=CONTENT_STATUS_PUBLISHED)
    
    def get_context_data(self, **kwargs): # http://stackoverflow.com/a/15515220
        context = super(PestReportListView, self).get_context_data(**kwargs)
        context['country'] = self.kwargs['country']
        # context.update({
        #     'country': self.kwargs['country']
        # })
        return context

# @login_required
# @permission_required('ippc.add_pestreport', login_url="/accounts/login/")

class PestReportHiddenListView(ListView):
    """
    Hidden Pest reports so editors can still edit them
    """
    context_object_name = 'latest'
    model = PestReport
    date_field = 'publish_date'
    template_name = 'countries/pest_report_hidden_list.html'
    queryset = PestReport.objects.all().order_by('-publish_date', 'title')
    allow_future = False
    allow_empty = True
    paginate_by = 30

    def get_queryset(self):
        """ only return pest reports from the specific country """
        # self.country = get_object_or_404(CountryPage, country=self.kwargs['country'])
        self.country = self.kwargs['country']
        # CountryPage country_slug == country URL parameter keyword argument
        return PestReport.objects.filter(country__country_slug=self.country, status=CONTENT_STATUS_DRAFT)
    
    def get_context_data(self, **kwargs): # http://stackoverflow.com/a/15515220
        context = super(PestReportHiddenListView, self).get_context_data(**kwargs)
        context['country'] = self.kwargs['country']
        # context.update({
        #     'country': self.kwargs['country']
        # })
        return context

    # put class-based generic view behind login
    # https://docs.djangoproject.com/en/dev/topics/class-based-views/intro/#decorating-the-class
    @method_decorator(login_required)
    @method_decorator(permission_required('ippc.add_pestreport', login_url="/accounts/login/"))
    def dispatch(self, *args, **kwargs):
        return super(PestReportHiddenListView, self).dispatch(*args, **kwargs)


class PestReportDetailView(DetailView):
    """ Pest report detail page """
    model = PestReport
    context_object_name = 'report'
    template_name = 'countries/pest_report_detail.html'
    queryset = PestReport.objects.filter(status=CONTENT_STATUS_PUBLISHED)
    # print('>>>>>>>>>>>>>>>')
    # print(user.get_profile().country)


class PublicationListView(ListView):
    """
    Publications List
    """
    context_object_name = 'latest'
    model = Publication
    date_field = 'modify_date'
    template_name = 'pages/publication_list.html'
    queryset = Publication.objects.filter(status=IS_PUBLIC).order_by('-modify_date', 'title')
    allow_future = False
    allow_empty = True
    paginate_by = 30

class PublicationDetailView(DetailView):
    """ Publication detail page """
    model = Publication
    context_object_name = 'publication'
    template_name = 'pages/publication_detail.html'
    queryset = Publication.objects.filter(status=IS_PUBLIC)


@login_required
@permission_required('ippc.add_pestreport', login_url="/accounts/login/")
def pest_report_create(request, country):
    """ Create Pest Report """
    user = request.user
    author = user
    country=user.get_profile().country
    user_country_slug = lower(slugify(country))

    form = PestReportForm(request.POST, request.FILES)
    
    if request.method == "POST":
        if form.is_valid():
            new_pest_report = form.save(commit=False)
            new_pest_report.author = request.user
            new_pest_report.author_id = author.id
            form.save()
            info(request, _("Successfully created pest report."))
            
            if new_pest_report.status == CONTENT_STATUS_DRAFT:
                return redirect("pest-report-hidden-list", country=user_country_slug)
            else:
                return redirect("pest-report-detail", country=user_country_slug, year=new_pest_report.publish_date.strftime("%Y"), month=new_pest_report.publish_date.strftime("%m"), slug=new_pest_report.slug)
    else:

        form = PestReportForm(initial={'country': country}, instance=PestReport())
    
    return render_to_response('countries/pest_report_create.html', {'form': form},
        context_instance=RequestContext(request))


# http://stackoverflow.com/a/1854453/412329
@login_required
@permission_required('ippc.change_pestreport', login_url="/accounts/login/")
def pest_report_edit(request, country, id=None, template_name='countries/pest_report_edit.html'):
    """ Edit Pest Report """
    user = request.user
    author = user
    country = user.get_profile().country
    # country_id = PestReport.objects.filter(country__country_id=country.id)
    user_country_slug = lower(slugify(country))
    
    if id:
        pest_report = get_object_or_404(PestReport, country=country, pk=id)
        # if pest_report.author != request.user:
        #     return HttpResponseForbidden()
    else:
        pest_report = PestReport(author=request.user)

    if request.POST:
        form = PestReportForm(request.POST,  request.FILES, instance=pest_report)

        if form.is_valid():
            form.save()

            # If the save was successful, success message and redirect to another page
            # info(request, _("Successfully updated pest report."))
            if pest_report.status == CONTENT_STATUS_DRAFT:
                return redirect("pest-report-hidden-list", country=user_country_slug)
            else:
                return redirect("pest-report-detail", country=user_country_slug, year=pest_report.publish_date.strftime("%Y"), month=pest_report.publish_date.strftime("%m"), slug=pest_report.slug)

    else:
        form = PestReportForm(instance=pest_report)

    return render_to_response(template_name, {
        'form': form, "pest_report": pest_report
    }, context_instance=RequestContext(request))


class BasicReportingListView(ListView):
    """    Basic Reporting """
    context_object_name = 'latest'
    model = BasicReporting
    date_field = 'publish_date'
    template_name = 'countries/basic_reporting_list.html'
    queryset = BasicReporting.objects.all().order_by('-publish_date', 'title')
    
    allow_future = False
    allow_empty = True
    paginate_by = 30

    def get_queryset(self):
        """ only return pest reports from the specific country """
        # self.country = get_object_or_404(CountryPage, country=self.kwargs['country'])
        self.country = self.kwargs['country']
        # CountryPage country_slug == country URL parameter keyword argument
        return BasicReporting.objects.filter(country__country_slug=self.country)
    
    def get_context_data(self, **kwargs): # http://stackoverflow.com/a/15515220
        context = super(BasicReportingListView, self).get_context_data(**kwargs)
        context['country'] = self.kwargs['country']
        context['basic_types'] =BASIC_REP_TYPE_CHOICES
        return context
   
       
   
class BasicReportingDetailView(DetailView):
    """  Basic Reporting detail page """
    model = BasicReporting
    context_object_name = 'basicreporting'
    template_name = 'countries/basic_reporting_detail.html'
    queryset = BasicReporting.objects.filter()
    #f3 = Files.objects.filter() 
   
    def get_context_data(self, **kwargs): # http://stackoverflow.com/a/15515220
        context = super(BasicReportingDetailView, self).get_context_data(**kwargs)
        return context


@login_required
@permission_required('ippc.add_basicreporting', login_url="/accounts/login/")
def basic_reporting_create(request, country,type):
    """ Create Basic Reporting """
    user = request.user
    author = user
    country=user.get_profile().country
    user_country_slug = lower(slugify(country))

    form = BasicReportingForm()
  
    if request.method == "POST":
        if form.is_valid():
            new_basic_reporting = form.save(commit=False)
            new_basic_reporting.author = request.user
            new_basic_reporting.author_id = author.id
            new_basic_reporting.basic_rep_type = type
            form.save()
            info(request, _("Successfully created basic_reporting."))
            
            return redirect("basic-reporting-detail", country=user_country_slug, year=new_basic_reporting.publish_date.strftime("%Y"), month=new_basic_reporting.publish_date.strftime("%m"), slug=new_basic_reporting.slug)
    else:
        form = BasicReportingForm(initial={'country': country,'basic_rep_type': type}, instance=BasicReporting())
    
    return render_to_response('countries/basic_reporting_create.html', {'form': form},
        context_instance=RequestContext(request))

        
# http://stackoverflow.com/a/1854453/412329
@login_required
@permission_required('ippc.change_basicreporting', login_url="/accounts/login/")
def basic_reporting_edit(request, country, id=None, template_name='countries/basic_reporting_edit.html'):
    """ Edit Basic Reporting """
    user = request.user
    author = user
    country = user.get_profile().country
    # country_id = PestReport.objects.filter(country__country_id=country.id)
    user_country_slug = lower(slugify(country))
    if id:
        basic_reporting = get_object_or_404(BasicReporting, country=country, pk=id)
        files=basic_reporting.getFiles()
        f=  get_object_or_404(Files,pk=files[0])
        f1=  get_object_or_404(Files,pk=files[1])
        aa=[]
        aa.append(f)
        aa.append(f1)
        
        # if pest_report.author != request.user:
        #     return HttpResponseForbidden()
    else:
        basic_reporting = BasicReporting(author=request.user)
      
    if request.POST:
        form = BasicReportingForm(request.POST,  request.FILES, instance=basic_reporting)
        filesform = [FilesForm(request.POST, request.FILES, prefix=str(x), instance=Files()) for x in range(0,2)]
        name='' 
        if form.is_valid() and all([ff.is_valid() for ff in filesform]):
            new_br = form.save(commit=False)
            #form.save()
            for ff in filesform:
                new_file = ff.save()
                if new_file.id!='' and new_file.id!='None':
                    name+=str(new_file.id)+','
                    new_br.file=name
                    form.save()
            form.save()
                        
            # If the save was successful, success message and redirect to another page
            # info(request, _("Successfully updated pest report."))
            return redirect("basic-reporting-detail", country=user_country_slug, year=basic_reporting.publish_date.strftime("%Y"), month=basic_reporting.publish_date.strftime("%m"), slug=basic_reporting.slug)

    else:
        form = BasicReportingForm(instance=basic_reporting)
       # all_forms = [MyModelForm(request.POST, prefix=str(id), instance=model.objects.get(pk=id)) for id in ids]
     
        filesform = [FilesForm(prefix=str(x), instance=aa[x]) for x in range(0,2)]
    return render_to_response(template_name, {
        'form': form, 'filesform': filesform, "basic_reporting": basic_reporting
    }, context_instance=RequestContext(request))
    

class EventReportingListView(ListView):
    """    Event Reporting """
    context_object_name = 'latest'
    model = BasicReporting
    date_field = 'publish_date'
    template_name = 'countries/event_reporting_list.html'
    queryset = EventReporting.objects.all().order_by('-publish_date', 'title')
    
    allow_future = False
    allow_empty = True
    paginate_by = 30

    def get_queryset(self):
        """ only return pest reports from the specific country """
        # self.country = get_object_or_404(CountryPage, country=self.kwargs['country'])
        self.country = self.kwargs['country']
        # CountryPage country_slug == country URL parameter keyword argument
        return EventReporting.objects.filter(country__country_slug=self.country)
    
    def get_context_data(self, **kwargs): # http://stackoverflow.com/a/15515220
        context = super(EventReportingListView, self).get_context_data(**kwargs)
        context['country'] = self.kwargs['country']
        context['event_types'] =EVT_REP_TYPE_CHOICES
        return context
   
       
   
class EventReportingDetailView(DetailView):
    """ EventReporting detail page """
    model = EventReporting
    context_object_name = 'eventreporting'
    template_name = 'countries/eventreporting_detail.html'
    queryset = EventReporting.objects.filter()
    # print('>>>>>>>>>>>>>>>')
    # print(user.get_profile().country)



@login_required
@permission_required('ippc.add_eventreporting', login_url="/accounts/login/")
def event_reporting_create(request, country,type):
    """ Create Event Reporting """
    user = request.user
    author = user
    country=user.get_profile().country
    user_country_slug = lower(slugify(country))

    form = EventReportingForm(request.POST or None, request.FILES)
  
    if request.method == "POST":
        if form.is_valid():
            new_event_reporting = form.save(commit=False)
            new_event_reporting.author = request.user
            new_event_reporting.author_id = author.id
            new_event_reporting.event_rep_type = type
            form.save()
            info(request, _("Successfully created event reporting."))
            
            return redirect("event-reporting-detail", country=user_country_slug, year=new_event_reporting.publish_date.strftime("%Y"), month=new_event_reporting.publish_date.strftime("%m"), slug=new_event_reporting.slug)
    else:
        form = EventReportingForm(initial={'country': country,'event_rep_type': type}, instance=EventReporting())
    
    return render_to_response('countries/event_reporting_create.html', {'form': form},
        context_instance=RequestContext(request))

        
# http://stackoverflow.com/a/1854453/412329
@login_required
@permission_required('ippc.change_eventreporting', login_url="/accounts/login/")
def event_reporting_edit(request, country, id=None, template_name='countries/event_reporting_edit.html'):
    """ Edit Basic Reporting """
    user = request.user
    author = user
    country = user.get_profile().country
    # country_id = PestReport.objects.filter(country__country_id=country.id)
    user_country_slug = lower(slugify(country))
    if id:
        event_reporting = get_object_or_404(EventReporting, country=country, pk=id)
        # if pest_report.author != request.user:
        #     return HttpResponseForbidden()
    else:
        event_reporting = EventReporting(author=request.user)
      
    if request.POST:
        form = EventReportingForm(request.POST,  request.FILES, instance=event_reporting)
        if form.is_valid():
            form.save()

            # If the save was successful, success message and redirect to another page
            info(request, _("Successfully updated pest report."))
            return redirect("event-reporting-detail", country=user_country_slug, year=event_reporting.publish_date.strftime("%Y"), month=event_reporting.publish_date.strftime("%m"), slug=event_reporting.slug)

    else:
        form = EventReportingForm(instance=event_reporting)

    return render_to_response(template_name, {
        'form': form, "event_reporting": event_reporting
    }, context_instance=RequestContext(request))
    
    
class PestFreeAreaListView(ListView):
    """    Event Reporting """
    context_object_name = 'latest'
    model = PestFreeArea
    date_field = 'publish_date'
    template_name = 'countries/pfa_list.html'
    queryset = PestFreeArea.objects.all().order_by('-publish_date', 'title')
    
    allow_future = False
    allow_empty = True
    paginate_by = 30

    def get_queryset(self):
        """ only return PestFreeArea from the specific country """
        # self.country = get_object_or_404(CountryPage, country=self.kwargs['country'])
        self.country = self.kwargs['country']
        # CountryPage country_slug == country URL parameter keyword argument
        return PestFreeArea.objects.filter(country__country_slug=self.country)
    
    def get_context_data(self, **kwargs): # http://stackoverflow.com/a/15515220
        context = super(PestFreeAreaListView, self).get_context_data(**kwargs)
        context['country'] = self.kwargs['country']
        return context
   
       
   
class PestFreeAreaDetailView(DetailView):
    """ PestFreeArea Detail page """
    model = PestFreeArea
    context_object_name = 'pfa'
    template_name = 'countries/pfa_detail.html'
    queryset = PestFreeArea.objects.filter()
    # print('>>>>>>>>>>>>>>>')
    # print(user.get_profile().country)



@login_required
@permission_required('ippc.add_pestfreearea', login_url="/accounts/login/")
def pfa_create(request, country):
    """ Create PestFreeArea """
    user = request.user
    author = user
    country=user.get_profile().country
    user_country_slug = lower(slugify(country))

    form = PestFreeAreaForm()
  
    if request.method == "POST":
        if form.is_valid():
            new_pfa = form.save(commit=False)
            new_pfa.author = request.user
            new_pfa.author_id = author.id
            form.save()
            info(request, _("Successfully created PestFreeArea."))
            
            return redirect("pfa-detail", country=user_country_slug, year=new_pfa.publish_date.strftime("%Y"), month=new_pfa.publish_date.strftime("%m"), slug=new_pfa.slug)
    else:
        form = PestFreeAreaForm(initial={'country': country}, instance=PestFreeArea())
    
    return render_to_response('countries/pfa_create.html', {'form': form},
        context_instance=RequestContext(request))

        
# http://stackoverflow.com/a/1854453/412329
@login_required
@permission_required('ippc.change_pestfreearea', login_url="/accounts/login/")
def pfa_edit(request, country, id=None, template_name='countries/pfa_edit.html'):
    """ Edit PestFreeArea """
    user = request.user
    author = user
    country = user.get_profile().country
    # country_id = PestReport.objects.filter(country__country_id=country.id)
    user_country_slug = lower(slugify(country))
    if id:
        pfa = get_object_or_404(PestFreeArea, country=country, pk=id)
        # if pest_report.author != request.user:
        #     return HttpResponseForbidden()
    else:
        pfa = PestFreeArea(author=request.user)
      
    if request.POST:
        form = PestFreeAreaForm(request.POST,  request.FILES, instance=pfa)
        if form.is_valid():
            form.save()

            # If the save was successful, success message and redirect to another page
            # info(request, _("Successfully updated pest report."))
            return redirect("pfa-detail", country=user_country_slug, year=pfa.publish_date.strftime("%Y"), month=pfa.publish_date.strftime("%m"), slug=pfa.slug)

    else:
        form = PestFreeAreaForm(instance=pfa)

    return render_to_response(template_name, {
        'form': form, "pfa": pfa
    }, context_instance=RequestContext(request))
    

class ImplementationISPMListView(ListView):
    """    ImplementationISPM """
    context_object_name = 'latest'
    model = ImplementationISPM
    date_field = 'publish_date'
    template_name = 'countries/implementationispm_list.html'
    queryset = ImplementationISPM.objects.all().order_by('-publish_date', 'title')
    
    allow_future = False
    allow_empty = True
    paginate_by = 30

    def get_queryset(self):
        """ only return pest reports from the specific country """
        # self.country = get_object_or_404(CountryPage, country=self.kwargs['country'])
        self.country = self.kwargs['country']
        # CountryPage country_slug == country URL parameter keyword argument
        return ImplementationISPM.objects.filter(country__country_slug=self.country)
    
    def get_context_data(self, **kwargs): # http://stackoverflow.com/a/15515220
        context = super(ImplementationISPMListView, self).get_context_data(**kwargs)
        context['country'] = self.kwargs['country']
        return context
   
       
   
class ImplementationISPMDetailView(DetailView):
    """ ImplementationISPM detail page """
    model = ImplementationISPM
    context_object_name = 'implementationispm'
    template_name = 'countries/implementationispm_detail.html'
    queryset = ImplementationISPM.objects.filter()
    # print('>>>>>>>>>>>>>>>')
    # print(user.get_profile().country)



@login_required
@permission_required('ippc.add_implementationispm', login_url="/accounts/login/")
def implementationispm_create(request, country):
    """ Create ImplementationISPM """
    user = request.user
    author = user
    country=user.get_profile().country
    user_country_slug = lower(slugify(country))

    form = ImplementationISPMForm()
  
    if request.method == "POST":
        if form.is_valid():
            new_implementationispm = form.save(commit=False)
            new_implementationispm.author = request.user
            new_implementationispm.author_id = author.id
            form.save()
            info(request, _("Successfully created implementationispm."))
            
            return redirect("implementationispm-detail", country=user_country_slug, year=new_implementationispm.publish_date.strftime("%Y"), month=new_implementationispm.publish_date.strftime("%m"), slug=new_implementationispm.slug)
    else:
        form = ImplementationISPMForm(initial={'country': country}, instance=ImplementationISPM())
    
    return render_to_response('countries/implementationispm_create.html', {'form': form},
        context_instance=RequestContext(request))

        
# http://stackoverflow.com/a/1854453/412329
@login_required
@permission_required('ippc.change_implementationispm', login_url="/accounts/login/")
def implementationispm_edit(request, country, id=None, template_name='countries/implementationispm_edit.html'):
    """ Edit implementationispm """
    user = request.user
    author = user
    country = user.get_profile().country
    # country_id = PestReport.objects.filter(country__country_id=country.id)
    user_country_slug = lower(slugify(country))
    if id:
        implementationispm = get_object_or_404(ImplementationISPM, country=country, pk=id)
        # if pest_report.author != request.user:
        #     return HttpResponseForbidden()
    else:
        implementationispm = ImplementationISPM(author=request.user)
      
    if request.POST:
        form = ImplementationISPMForm(request.POST,  request.FILES, instance=implementationispm)
        if form.is_valid():
            form.save()

            # If the save was successful, success message and redirect to another page
            # info(request, _("Successfully updated pest report."))
            return redirect("implementationispm-detail", country=user_country_slug, year=implementationispm.publish_date.strftime("%Y"), month=implementationispm.publish_date.strftime("%m"), slug=implementationispm.slug)

    else:
        form = ImplementationISPMForm(instance=implementationispm)

    return render_to_response(template_name, {
        'form': form, "implementationispm": implementationispm
    }, context_instance=RequestContext(request))
    
class CountryListView(ListView):
    """   alphabetic countries list  """
    context_object_name = 'latest'
    model = CountryPage
    template_name = 'countries/countries_list.html'
    queryset = CountryPage.objects.all().order_by('title')
    #region_name=self.kwargs['region']
   
    def get_context_data(self, **kwargs): # http://stackoverflow.com/a/15515220
        context = super(CountryListView, self).get_context_data(**kwargs)
        context['number_of_cp']= CountryPage.objects.filter(cp_ncp_t_type='CP').count()
        if self.kwargs['region'] == 'all':
            context['countries']= CountryPage.objects.all()
        else:
            for k,v in REGIONS:
                reg = v.lower()
                reg = reg.replace(" ", "-");
                if reg == self.kwargs['region']:
                    kindex=k
                    context['region_name']=v
            context['countries']= CountryPage.objects.filter(region=kindex)
        return context

class AdvancesSearchCNListView(ListView):
    """  AdvancesSearchCNListView list  """
    context_object_name = 'latest'
    model = CountryPage
    template_name = 'countries/countries_advsearchresults.html'
    
    def get_context_data(self, **kwargs): # http://stackoverflow.com/a/15515220
        context = super(AdvancesSearchCNListView, self).get_context_data(**kwargs)
        if self.kwargs['type'] == 'pestreport':
            context['type_label'] = 'Official pest report (Art. VIII.1a)'
            context['link_to_item'] = 'pest-report-detail'
            context['items']= PestReport.objects.all()
            context['counttotal'] =context['items'].count() 
        elif self.kwargs['type'] == 'nppo':
            context['type_label'] = dict(BASIC_REP_TYPE_CHOICES)[1]
            context['link_to_item'] = 'basic-reporting-detail'
            context['items']= BasicReporting.objects.filter(basic_rep_type=1)
            context['counttotal'] =context['items'].count() 
        elif self.kwargs['type'] == 'entrypoints':
            context['type_label'] = dict(BASIC_REP_TYPE_CHOICES)[2]
            context['link_to_item'] = 'basic-reporting-detail'
            context['items']= BasicReporting.objects.filter(basic_rep_type=2)
            context['counttotal'] =context['items'].count() 
        elif self.kwargs['type'] == 'regulatedpests':
            context['type_label'] = dict(BASIC_REP_TYPE_CHOICES)[3]
            context['link_to_item'] = 'basic-reporting-detail'
            context['items']= BasicReporting.objects.filter(basic_rep_type=3)
            context['counttotal'] =context['items'].count() 
        elif self.kwargs['type'] == 'legislation':
            context['type_label'] = dict(BASIC_REP_TYPE_CHOICES)[4]
            context['link_to_item'] = 'basic-reporting-detail'
            context['items']= BasicReporting.objects.filter(basic_rep_type=4)
            context['counttotal'] =context['items'].count() 
        elif self.kwargs['type'] == 'emergencyactions':
            context['type_label'] = dict(EVT_REP_TYPE_CHOICES)[1]
            context['link_to_item'] = 'event-reporting-detail'
            context['items']= EventReporting.objects.filter(event_rep_type=1)
            context['counttotal'] =context['items'].count() 
        elif self.kwargs['type'] == 'noncompliance':
            context['type_label'] = dict(EVT_REP_TYPE_CHOICES)[2]
            context['link_to_item'] = 'event-reporting-detail'
            context['items']= EventReporting.objects.filter(event_rep_type=2)
            context['counttotal'] =context['items'].count() 
        elif self.kwargs['type'] == 'plantprotection':
            context['type_label'] = dict(EVT_REP_TYPE_CHOICES)[3]
            context['link_to_item'] = 'event-reporting-detail'
            context['items']= EventReporting.objects.filter(event_rep_type=3)
            context['counttotal'] =context['items'].count() 
        elif self.kwargs['type'] == 'peststatus':
            context['type_label'] = dict(EVT_REP_TYPE_CHOICES)[4]
            context['link_to_item'] = 'event-reporting-detail'
            context['items']= EventReporting.objects.filter(event_rep_type=4)
            context['counttotal'] =context['items'].count() 
        elif self.kwargs['type'] == 'phytosanitaryrequirements':
            context['type_label'] = dict(EVT_REP_TYPE_CHOICES)[5]
            context['link_to_item'] = 'event-reporting-detail'
            context['items']= EventReporting.objects.filter(event_rep_type=5)
            context['counttotal'] =context['items'].count() 
        elif self.kwargs['type'] == 'pfa':
            context['type_label'] = 'Pest free areas'
            context['link_to_item'] = 'pfa-detail'
            context['items']= PestFreeArea.objects.all()
            context['counttotal'] =context['items'].count() 
        elif self.kwargs['type'] == 'ispm15':
            context['type_label'] = 'Implementation of ISPM 15'
            context['link_to_item'] = 'implementationispm-detail'
            context['items']= ImplementationISPM.objects.all()
            context['counttotal'] =context['items'].count() 
        
        
        
        return context
		
		
		
	