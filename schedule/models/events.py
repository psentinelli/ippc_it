# -*- coding: utf-8 -*-
from django.conf import settings as django_settings
import pytz
from dateutil import rrule

from django.contrib.contenttypes import generic
from django.db import models
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.template.defaultfilters import date
from django.utils.translation import ugettext, ugettext_lazy as _
from django.utils import timezone

from schedule.conf import settings
from schedule.models.rules import Rule
from schedule.models.calendars import Calendar
from schedule.utils import OccurrenceReplacer
from django.contrib.contenttypes.generic import GenericRelation

from ippc.models import IssueKeywordsRelate,validate_file_extension, CountryPage, PartnersPage, REGIONS, Topic
from django.contrib.auth.models import User, Group

class EventManager(models.Manager):
    def get_for_object(self, content_object, distinction=None, inherit=True):
        return EventRelation.objects.get_events_for_object(content_object, distinction, inherit)

EVENT_CAT_1 = 1
EVENT_CAT_2 = 2
EVENT_CAT_3 = 3
EVENT_CAT_4 = 4
EVENT_CAT_5 = 5
EVENT_CAT_6 = 6
EVENT_CAT_7 = 7
CATEGORIES = (
    (EVENT_CAT_1, (" ")),
    (EVENT_CAT_2, _("Standards")),
    (EVENT_CAT_3, _("Dispute Settlement")),
    (EVENT_CAT_4, _("Governance")),
    (EVENT_CAT_5, _("Information Exchange")),
    (EVENT_CAT_6, _("RPPO")),
    (EVENT_CAT_7, _("Capacity building")),
    
)
EVENT_TYPE_1 = 1
EVENT_TYPE_2 = 2
EVENT_TYPE_3 = 3
EVENT_TYPE_4 = 4
EVENT_TYPE_5 = 5
EVENT_TYPE_6 = 6
EVENT_TYPE_7 = 7
EVENT_TYPE_8 = 8
EVENT_TYPE_9 = 9
EVENT_TYPE_10 = 10
EVENT_TYPE_11 = 11
EVENT_TYPE_12 = 12
EVENT_TYPE_13 = 13
EVENT_TYPE_14 = 14
EVENT_TYPE_15 = 15
EVENT_TYPE_16 = 16
EVENT_TYPE_17 = 17
EVENT_TYPE_18 = 18
EVENT_TYPE_19 = 19
EVENT_TYPE_20 = 20
EVENT_TYPE_21 = 21
EVENT_TYPE_22 = 22
EVENT_TYPE_23 = 23
EVENT_TYPE_24 = 24
EVENT_TYPE_25 = 25
EVENT_TYPE_26 = 26
EVENT_TYPE_27 = 27
EVENT_TYPE_28 = 28
EVENT_TYPE_29 = 29
EVENT_TYPE_30 = 30
EVENT_TYPE_31 = 31
EVENT_TYPE_32 = 32
EVENT_TYPE_33 = 33
TYPES = (
    (EVENT_TYPE_1, (" ")),
    (EVENT_TYPE_2, _("Bilateral assistance")),
    (EVENT_TYPE_3, _("Bureau")),
    (EVENT_TYPE_4, _("CBD")),
    (EVENT_TYPE_5, _("CDC + Expert Working Group on Capacity Building")),
    (EVENT_TYPE_6, _("Conference")),
    (EVENT_TYPE_7, _("CPM")),
    (EVENT_TYPE_8, _("Expert Consultation")),
    (EVENT_TYPE_9, _("Expert Working Group")),
    (EVENT_TYPE_10, _("Finance Committee")),
    (EVENT_TYPE_11, _("Focus Group")),
    (EVENT_TYPE_12, _("IRSS")),
    (EVENT_TYPE_13, _("Consultation")),
    (EVENT_TYPE_14, _("Mentoring / Assistance")),
    (EVENT_TYPE_15, _("NRO")),
    (EVENT_TYPE_16, _("NRO Advidory Group")),
    (EVENT_TYPE_17, _("Other")),
    (EVENT_TYPE_18, _("Other Working Group")),
    (EVENT_TYPE_19, _("Regional Workshops on Draft ISPMs")),
    (EVENT_TYPE_33, _("Regional Workshops")),
    (EVENT_TYPE_32, _("Resource Mobilization")),
    (EVENT_TYPE_20, _("SBDS")),
    (EVENT_TYPE_21, _("Seminar")),
    (EVENT_TYPE_22, _("SPG + SPTA")),
    (EVENT_TYPE_23, _("Standards Committee")),
    (EVENT_TYPE_24, _("Symposium")),
    (EVENT_TYPE_25, _("Technical Consultation of RPPOs")),
    (EVENT_TYPE_26, _("Technical Panel")),
    (EVENT_TYPE_27, _("Training")),
    (EVENT_TYPE_28, _("Workshop")),
    (EVENT_TYPE_29, _("Workshop / Seminars")),
    (EVENT_TYPE_30, _("WTO Meetings")),
    (EVENT_TYPE_31, _("SPG")),
)

class Event(models.Model):
    '''
    This model stores meta data for a date.  You can relate this data to many
    other models.
    '''
    title = models.CharField(_("Title"), max_length=255)
    start = models.DateTimeField(_("Start"), blank=True, null=True, editable=True)
    end = models.DateTimeField(_("End"), help_text=_("The end time must be later than the start time."))
   
    category = models.IntegerField(_("Category"), choices=CATEGORIES, default=None)
    type = models.IntegerField(_("Type"), choices=TYPES,default=None)
    
    description = models.TextField(_("description"), null=True, blank=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, verbose_name=_("creator"),
                                related_name='creator')
    created_on = models.DateTimeField(_("created on"), auto_now_add=True)
    updated_on = models.DateTimeField(_("updated on"), auto_now=True)
    rule = models.ForeignKey(Rule, null=True, blank=True, verbose_name=_("rule"),
                             help_text=_("Select '----' for a one time only event."))
    end_recurring_period = models.DateTimeField(_("end recurring period"), null=True, blank=True,
                                                help_text=_("This date is ignored for one time only events."))
    calendar = models.ForeignKey(Calendar, null=True, blank=True, verbose_name=_("calendar"))
    location = models.CharField(_("Location"), max_length=255,blank=True, null=True)
    venuecity = models.CharField(_("Venue City"), max_length=255,blank=True, null=True)
    venuecountry = models.CharField(_("Venue Country"), max_length=255,blank=True, null=True)
    organizer = models.CharField(_("Organizer"), max_length=255,blank=True, null=True)
    issuename=generic.GenericRelation(IssueKeywordsRelate)
    country = models.ForeignKey(CountryPage, related_name="event_country_page", default=-1)
    can_register = models.BooleanField(_("Users can register"), default=False, help_text=_("Check this if you want that users can register to this Event."))
    end_register_date = models.DateTimeField(_("End registration date"), null=True, blank=True,
                                                help_text=_("Users won't be able to register after this date."))
    groups = models.ManyToManyField(Group, 
        verbose_name=_("Groups that can register to this event"), 
        related_name='evparticipantgroups', blank=True, null=True)
    topic_numbers = models.ManyToManyField( Topic, 
        verbose_name=_("Select all the topic numbers that apply"), 
        related_name='ev_topic_numbers', blank=True, null=True)
    objects = EventManager()

    class Meta:
        verbose_name = _('event')
        verbose_name_plural = _('events')
        app_label = 'schedule'

    def __unicode__(self):
        date_format = u'%s' % ugettext("DATE_FORMAT")
        return ugettext('%(title)s: %(start)s - %(end)s') % {
            'title': self.title,
            'start': date(self.start, date_format),
            'end': date(self.end, date_format),
        }
    def category_verbose(self):
        return dict(CATEGORIES)[self.category]
    def type_verbose(self):
        return dict(TYPES)[self.type]
    def get_array_participants(self):
        array_participants=[]    
        eventParticipants=EventParticipants.objects.filter(event_id=self.id)
        for u in eventParticipants:
           array_participants.append(u.user)
        return array_participants
    def get_absolute_url(self):
        return reverse('event', args=[self.id])
    def is_not_past_due(self):
        if timezone.now() <= self.end_register_date:
            return True
        else: 
            return False   
    def get_occurrences(self, start, end):
        """
        >>> rule = Rule(frequency = "MONTHLY", name = "Monthly")
        >>> rule.save()
        >>> event = Event(rule=rule, start=datetime.datetime(2008,1,1,tzinfo=pytz.utc), end=datetime.datetime(2008,1,2))
        >>> event.rule
        <Rule: Monthly>
        >>> occurrences = event.get_occurrences(datetime.datetime(2008,1,24), datetime.datetime(2008,3,2))
        >>> ["%s to %s" %(o.start, o.end) for o in occurrences]
        ['2008-02-01 00:00:00+00:00 to 2008-02-02 00:00:00+00:00', '2008-03-01 00:00:00+00:00 to 2008-03-02 00:00:00+00:00']

        Ensure that if an event has no rule, that it appears only once.

        >>> event = Event(start=datetime.datetime(2008,1,1,8,0), end=datetime.datetime(2008,1,1,9,0))
        >>> occurrences = event.get_occurrences(datetime.datetime(2008,1,24), datetime.datetime(2008,3,2))
        >>> ["%s to %s" %(o.start, o.end) for o in occurrences]
        []
`
        """
        if self.pk:
            # performance booster for occurrences relationship
            Event.objects.select_related('occurrence').get(pk=self.pk)
        persisted_occurrences = self.occurrence_set.all()
        occ_replacer = OccurrenceReplacer(persisted_occurrences)
        occurrences = self._get_occurrence_list(start, end)
        final_occurrences = []
        for occ in occurrences:
            # replace occurrences with their persisted counterparts
            if occ_replacer.has_occurrence(occ):
                p_occ = occ_replacer.get_occurrence(occ)
                # ...but only if they are within this period
                if p_occ.start < end and p_occ.end >= start:
                    final_occurrences.append(p_occ)
            else:
                final_occurrences.append(occ)
        # then add persisted occurrences which originated outside of this period but now
        # fall within it
        final_occurrences += occ_replacer.get_additional_occurrences(start, end)
        return final_occurrences

    def get_rrule_object(self):
        if self.rule is not None:
            params = self.rule.get_params()
            frequency = self.rule.rrule_frequency()
            return rrule.rrule(frequency, dtstart=self.start, **params)

    def _create_occurrence(self, start, end=None):
        if end is None:
            end = start + (self.end - self.start)
        return Occurrence(event=self, start=start, end=end, original_start=start, original_end=end)

    def get_occurrence(self, date):
        if timezone.is_naive(date) and django_settings.USE_TZ:
            date = timezone.make_aware(date, timezone.utc)
        rule = self.get_rrule_object()
        if rule:
            next_occurrence = rule.after(date, inc=True)
        else:
            next_occurrence = self.start
        if next_occurrence == date:
            try:
                return Occurrence.objects.get(event=self, original_start=date)
            except Occurrence.DoesNotExist:
                return self._create_occurrence(next_occurrence)

    def _get_occurrence_list(self, start, end):
        """
        returns a list of occurrences for this event from start to end.
        """
        difference = (self.end - self.start)
        if self.rule is not None:
            occurrences = []
            if self.end_recurring_period and self.end_recurring_period < end:
                end = self.end_recurring_period
            rule = self.get_rrule_object()
            o_starts = rule.between(start - difference, end - difference, inc=True)
            for o_start in o_starts:
                o_end = o_start + difference
                occurrences.append(self._create_occurrence(o_start, o_end))
            return occurrences
        else:
            # check if event is in the period
            if self.start < end and self.end > start:
                return [self._create_occurrence(self.start)]
            else:
                return []

    def _occurrences_after_generator(self, after=None, tzinfo=pytz.utc):
        """
        returns a generator that produces unpresisted occurrences after the
        datetime ``after``.
        """

        if after is None:
            after = timezone.now()
        rule = self.get_rrule_object()
        if rule is None:
            if self.end > after:
                yield self._create_occurrence(self.start, self.end)
            raise StopIteration
        date_iter = iter(rule)
        difference = self.end - self.start
        while True:
            o_start = date_iter.next()
            if o_start > self.end_recurring_period:
                raise StopIteration
            o_end = o_start + difference
            if o_end > after:
                yield self._create_occurrence(o_start, o_end)

    def occurrences_after(self, after=None):
        """
        returns a generator that produces occurrences after the datetime
        ``after``.  Includes all of the persisted Occurrences.
        """
        occ_replacer = OccurrenceReplacer(self.occurrence_set.all())
        generator = self._occurrences_after_generator(after)
        while True:
            next = generator.next()
            yield occ_replacer.get_occurrence(next)

class EventFile(models.Model):
    event = models.ForeignKey(Event, verbose_name=_("event"))
    description = models.CharField(max_length=255)
    file = models.FileField(max_length=255,blank=True, help_text='10 MB maximum file size.', verbose_name='Upload a file', upload_to='files/event/%Y/%m/%d/', validators=[validate_file_extension])

    def __unicode__(self):  
        return self.file.name  
    def name(self):
        return self.file.name
    def filename(self):
        return os.path.basename(self.file.name) 
    def fileextension(self):
        return os.path.splitext(self.file.name)[1]
    class Meta:
        verbose_name = _("event file")
        verbose_name_plural = _("event files")
        app_label = 'schedule'
class EventUrl(models.Model):
    event = models.ForeignKey(Event, verbose_name=_("event"))
    #url = models.UrlField(blank=True, null=True)
    url_for_more_information = models.URLField(blank=True, null=True)
    def __unicode__(self):  
        return self.url_for_more_information  
    def name(self):
        return self.url_for_more_information
   
    class Meta:
        verbose_name = _("event url")
        verbose_name_plural = _("event urls")
        app_label = 'schedule'
                        

FUND_TYPE_0 =0
FUND_TYPE_1 = 1
FUND_TYPE_2 =2
FUNDS = (
    (FUND_TYPE_0, _("No funding")),
    (FUND_TYPE_1, _("Airfare funding")),
    (FUND_TYPE_2, _("Airfare and DSA funding")),
)  
BOOL_CHOICES_1 = True
BOOL_CHOICES_2 = False
BOOL_CHOICES = (
    (BOOL_CHOICES_1, _("Yes")),
    (BOOL_CHOICES_2, _("No")),
)


BOOL_CHOICES2_1 = True
BOOL_CHOICES2_2 = False
BOOL_CHOICES2 = (
    (BOOL_CHOICES2_1, _(u"\u2713")),
    (BOOL_CHOICES2_2, _(" ")),
)

class ParticipantRoles(models.Model):
    """ Participant Role """
    role = models.CharField(_("Role"), max_length=500)

    def __unicode__(self):
        return self.role
        
    class Meta:
        verbose_name = _("Participant Role")
        verbose_name_plural = _("Participant Roles")
        app_label = 'schedule'
    pass
        
class EventParticipants(models.Model):
    event = models.ForeignKey(Event, verbose_name=_("event"))
    
    user = models.ForeignKey(User,verbose_name=_("User"), blank=True, null=True)
    role = models.ManyToManyField(ParticipantRoles,
        verbose_name=_("Role"),
        related_name='role+', blank=True, null=True,)
        
    attended = models.NullBooleanField(_("Attended"), choices=BOOL_CHOICES,blank=True, null=True,)
    registered = models.NullBooleanField(_("Registered"), choices=BOOL_CHOICES,blank=True, null=True,)
    registered_date =models.DateTimeField(_("Registered date"), blank=True, null=True, editable=True)
    #funding =  models.IntegerField(_("Funding"), choices=FUNDS, default=None,blank=True, null=True)

    representing_country = models.ForeignKey(CountryPage,  verbose_name=_("Representing Country "), blank=True, null=True )
    representing_organization = models.ForeignKey(PartnersPage,  verbose_name=_("Representing Organization"), blank=True, null=True)
    representing_region =   models.IntegerField(_("Representing FAO Region"), choices=REGIONS, default=None,blank=True, null=True)

    class Meta:
        verbose_name = _("Event Participant")
        verbose_name_plural = _("Event Participant")
        app_label = 'schedule'
    #def __unicode__(self):  
   #     return self.user.id 
   # def name(self):
  #      return self.user
   
  
      
    def participant_registered_verbose(self):
        if self.registered != None:
            return dict(BOOL_CHOICES2)[self.registered]
        else:
            return ''
    def participant_attended_verbose(self):
        if self.attended != None:
            return dict(BOOL_CHOICES2)[self.attended]
        else:
            return ''    
    def participant_funding_verbose(self):
        if self.funding != None:
            return dict(FUNDS)[self.funding]
        else:
            return ''
    def representing_region_verbose(self):
        if self.representing_region != None:
            return dict(REGIONS)[self.representing_region]
        else:
            return ''    
        
        
  
class EventRelationManager(models.Manager):
    '''
    >>> EventRelation.objects.all().delete()
    >>> CalendarRelation.objects.all().delete()
    >>> data = {
    ...         'title': 'Test1',
    ...         'start': datetime.datetime(2008, 1, 1),
    ...         'end': datetime.datetime(2008, 1, 11)
    ...        }
    >>> Event.objects.all().delete()
    >>> event1 = Event(**data)
    >>> event1.save()
    >>> data['title'] = 'Test2'
    >>> event2 = Event(**data)
    >>> event2.save()
    >>> user1 = User(username='alice')
    >>> user1.save()
    >>> user2 = User(username='bob')
    >>> user2.save()
    >>> event1.create_relation(user1, 'owner')
    >>> event1.create_relation(user2, 'viewer')
    >>> event2.create_relation(user1, 'viewer')
    '''
    # Currently not supported
    # Multiple level reverse lookups of generic relations appears to be
    # unsupported in Django, which makes sense.
    #
    # def get_objects_for_event(self, event, model, distinction=None):
    #     '''
    #     returns a queryset full of instances of model, if it has an EventRelation
    #     with event, and distinction
    #     >>> event = Event.objects.get(title='Test1')
    #     >>> EventRelation.objects.get_objects_for_event(event, User, 'owner')
    #     [<User: alice>]
    #     >>> EventRelation.objects.get_objects_for_event(event, User)
    #     [<User: alice>, <User: bob>]
    #     '''
    #     if distinction:
    #         dist_q = Q(eventrelation__distinction = distinction)
    #     else:
    #         dist_q = Q()
    #     ct = ContentType.objects.get_for_model(model)
    #     return model.objects.filter(
    #         dist_q,
    #         eventrelation__content_type = ct,
    #         eventrelation__event = event
    #     )

    def get_events_for_object(self, content_object, distinction=None, inherit=True):
        '''
        returns a queryset full of events, that relate to the object through, the
        distinction

        If inherit is false it will not consider the calendars that the events
        belong to. If inherit is true it will inherit all of the relations and
        distinctions that any calendar that it belongs to has, as long as the
        relation has inheritable set to True.  (See Calendar)

        >>> event = Event.objects.get(title='Test1')
        >>> user = User.objects.get(username = 'alice')
        >>> EventRelation.objects.get_events_for_object(user, 'owner', inherit=False)
        [<Event: Test1: Tuesday, Jan. 1, 2008-Friday, Jan. 11, 2008>]

        If a distinction is not declared it will not vet the relations based on
        distinction.
        >>> EventRelation.objects.get_events_for_object(user, inherit=False)
        [<Event: Test1: Tuesday, Jan. 1, 2008-Friday, Jan. 11, 2008>, <Event: Test2: Tuesday, Jan. 1, 2008-Friday, Jan. 11, 2008>]

        Now if there is a Calendar
        >>> calendar = Calendar(name = 'MyProject')
        >>> calendar.save()

        And an event that belongs to that calendar
        >>> event = Event.objects.get(title='Test2')
        >>> calendar.events.add(event)

        If we relate this calendar to some object with inheritable set to true,
        that relation will be inherited
        >>> user = User.objects.get(username='bob')
        >>> cr = calendar.create_relation(user, 'viewer', True)
        >>> EventRelation.objects.get_events_for_object(user, 'viewer')
        [<Event: Test1: Tuesday, Jan. 1, 2008-Friday, Jan. 11, 2008>, <Event: Test2: Tuesday, Jan. 1, 2008-Friday, Jan. 11, 2008>]
        '''
        ct = ContentType.objects.get_for_model(type(content_object))
        if distinction:
            dist_q = Q(eventrelation__distinction=distinction)
            cal_dist_q = Q(calendar__calendarrelation__distinction=distinction)
        else:
            dist_q = Q()
            cal_dist_q = Q()
        if inherit:
            inherit_q = Q(
                cal_dist_q,
                calendar__calendarrelation__object_id=content_object.id,
                calendar__calendarrelation__content_type=ct,
                calendar__calendarrelation__inheritable=True,
            )
        else:
            inherit_q = Q()
        event_q = Q(dist_q, Q(eventrelation__object_id=content_object.id), Q(eventrelation__content_type=ct))
        return Event.objects.filter(inherit_q | event_q)

    def create_relation(self, event, content_object, distinction=None):
        """
        Creates a relation between event and content_object.
        See EventRelation for help on distinction.
        """
        ct = ContentType.objects.get_for_model(type(content_object))
        object_id = content_object.id
        er = EventRelation(
            content_type=ct,
            object_id=object_id,
            event=event,
            distinction=distinction,
            content_object=content_object
        )
        er.save()
        return er


class EventRelation(models.Model):
    '''
    This is for relating data to an Event, there is also a distinction, so that
    data can be related in different ways.  A good example would be, if you have
    events that are only visible by certain users, you could create a relation
    between events and users, with the distinction of 'visibility', or
    'ownership'.

    event: a foreign key relation to an Event model.
    content_type: a foreign key relation to ContentType of the generic object
    object_id: the id of the generic object
    content_object: the generic foreign key to the generic object
    distinction: a string representing a distinction of the relation, User could
    have a 'veiwer' relation and an 'owner' relation for example.

    DISCLAIMER: while this model is a nice out of the box feature to have, it
    may not scale well.  If you use this keep that in mindself.
    '''
    event = models.ForeignKey(Event, verbose_name=_("event"))
    content_type = models.ForeignKey(ContentType)
    object_id = models.IntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    distinction = models.CharField(_("distinction"), max_length=20, null=True)

    objects = EventRelationManager()

    class Meta:
        verbose_name = _("event relation")
        verbose_name_plural = _("event relations")
        app_label = 'schedule'

    def __unicode__(self):
        return u'%s(%s)-%s' % (self.event.title, self.distinction, self.content_object)


class Occurrence(models.Model):
    event = models.ForeignKey(Event, verbose_name=_("event"))
    title = models.CharField(_("title"), max_length=255, blank=True, null=True)
    description = models.TextField(_("description"), blank=True, null=True)
    start = models.DateTimeField(_("start"))
    end = models.DateTimeField(_("end"))
    cancelled = models.BooleanField(_("cancelled"), default=False)
    original_start = models.DateTimeField(_("original start"))
    original_end = models.DateTimeField(_("original end"))
    created_on = models.DateTimeField(_("created on"), auto_now_add=True)
    updated_on = models.DateTimeField(_("updated on"), auto_now=True)

    class Meta:
        verbose_name = _("occurrence")
        verbose_name_plural = _("occurrences")
        app_label = 'schedule'

    def __init__(self, *args, **kwargs):
        super(Occurrence, self).__init__(*args, **kwargs)
        if self.title is None and self.event_id:
            self.title = self.event.title
        if self.description is None and self.event_id:
            self.description = self.event.description

    def moved(self):
        return self.original_start != self.start or self.original_end != self.end

    moved = property(moved)

    def move(self, new_start, new_end):
        self.start = new_start
        self.end = new_end
        self.save()

    def cancel(self):
        self.cancelled = True
        self.save()

    def uncancel(self):
        self.cancelled = False
        self.save()

    def get_absolute_url(self):
        if self.pk is not None:
            return reverse('occurrence', kwargs={'occurrence_id': self.pk,
                                                 'event_id': self.event.id})
        return reverse('occurrence_by_date', kwargs={
            'event_id': self.event.id,
            'year': self.start.year,
            'month': self.start.month,
            'day': self.start.day,
            'hour': self.start.hour,
            'minute': self.start.minute,
            'second': self.start.second,
        })

    def get_cancel_url(self):
        if self.pk is not None:
            return reverse('cancel_occurrence', kwargs={'occurrence_id': self.pk,
                                                        'event_id': self.event.id})
        return reverse('cancel_occurrence_by_date', kwargs={
            'event_id': self.event.id,
            'year': self.start.year,
            'month': self.start.month,
            'day': self.start.day,
            'hour': self.start.hour,
            'minute': self.start.minute,
            'second': self.start.second,
        })

    def get_edit_url(self):
        if self.pk is not None:
            return reverse('edit_occurrence', kwargs={'occurrence_id': self.pk,
                                                      'event_id': self.event.id})
        return reverse('edit_occurrence_by_date', kwargs={
            'event_id': self.event.id,
            'year': self.start.year,
            'month': self.start.month,
            'day': self.start.day,
            'hour': self.start.hour,
            'minute': self.start.minute,
            'second': self.start.second,
        })

    def __unicode__(self):
        return ugettext("%(start)s to %(end)s") % {
            'start': self.start,
            'end': self.end,
        }

    def __cmp__(self, other):
        rank = cmp(self.start, other.start)
        if rank == 0:
            return cmp(self.end, other.end)
        return rank

    def __eq__(self, other):
        return (isinstance(other, Occurrence) and
                self.original_start == other.original_start and self.original_end == other.original_end)


