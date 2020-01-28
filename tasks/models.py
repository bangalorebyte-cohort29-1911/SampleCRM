import arrow
from django.db import models
from common.models import User
from contacts.models import Contact
from django.utils.translation import ugettext_lazy as _
from teams.models import Teams
from django.utils.translation import pgettext_lazy
from common.utils import INDCHOICES, COUNTRIES
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.text import slugify


class Tags(models.Model):
    name = models.CharField(max_length=20)
    slug = models.CharField(max_length=20, unique=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Tags, self).save(*args, **kwargs)


class Account(models.Model):

    ACCOUNT_STATUS_CHOICE = (
        ("open", "Open"),
        ('close', 'Close')
    )

    name = models.CharField(pgettext_lazy(
        "Name of Account", "Name"), max_length=64)
    email = models.EmailField()
    phone = PhoneNumberField(null=True)
    industry = models.CharField(
        _("Industry Type"),
        max_length=255, choices=INDCHOICES,
        blank=True, null=True)
    website = models.URLField(_("Website"), blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(
        User, related_name='account_created_by',
        on_delete=models.SET_NULL, null=True)
    created_on = models.DateTimeField(_("Created on"), auto_now_add=True)
    is_active = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tags, blank=True)
    status = models.CharField(
        choices=ACCOUNT_STATUS_CHOICE, max_length=64, default='open')
    lead = models.ForeignKey(
        'leads.Lead', related_name="account_leads",
        on_delete=models.SET_NULL, null=True)
    contact_name = models.CharField(pgettext_lazy(
        "Name of Contact", "Contact Name"), max_length=120)
    contacts = models.ManyToManyField(
        'contacts.Contact', related_name="account_contacts")
    assigned_to = models.ManyToManyField(
        User, related_name='account_assigned_users')
    teams = models.ManyToManyField(Teams, related_name='account_teams')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_on']

    @property
    def created_on_arrow(self):
        return arrow.get(self.created_on).humanize()

    @property
    def contact_values(self):
        contacts = list(self.contacts.values_list('id', flat=True))
        return ','.join(str(contact) for contact in contacts)

    @property
    def get_team_users(self):
        team_user_ids = list(self.teams.values_list('users__id', flat=True))
        return User.objects.filter(id__in=team_user_ids)

    @property
    def get_team_and_assigned_users(self):
        team_user_ids = list(self.teams.values_list('users__id', flat=True))
        assigned_user_ids = list(self.assigned_to.values_list('id', flat=True))
        user_ids = team_user_ids + assigned_user_ids
        return User.objects.filter(id__in=user_ids)

    @property
    def get_assigned_users_not_in_teams(self):
        team_user_ids = list(self.teams.values_list('users__id', flat=True))
        assigned_user_ids = list(self.assigned_to.values_list('id', flat=True))
        user_ids = set(assigned_user_ids) - set(team_user_ids)
        return User.objects.filter(id__in=list(user_ids))



class Task(models.Model):

    STATUS_CHOICES = (
        ("New", "New"),
        ("In Progress", "In Progress"),
        ("Completed", "Completed")
    )

    PRIORITY_CHOICES = (
        ("Low", "Low"),
        ("Medium", "Medium"),
        ("High", "High")
    )

    title = models.CharField(_("title"), max_length=200)
    status = models.CharField(
        _("status"), max_length=50, choices=STATUS_CHOICES)
    priority = models.CharField(
        _("priority"), max_length=50, choices=PRIORITY_CHOICES)
    due_date = models.DateField(blank=True, null=True)
    created_on = models.DateTimeField(_("Created on"), auto_now_add=True)
    account = models.ForeignKey(
        Account, related_name='accounts', null=True, blank=True, on_delete=models.SET_NULL)

    contacts = models.ManyToManyField(
        Contact, related_name="contacts_tasks")

    assigned_to = models.ManyToManyField(
        User, related_name='users_tasks')

    created_by = models.ForeignKey(
        User, related_name='task_created', blank=True, null=True, on_delete=models.SET_NULL)
    teams = models.ManyToManyField(Teams, related_name='tasks_teams')


    def __str__(self):
        return self.title

    @property
    def created_on_arrow(self):
        return arrow.get(self.created_on).humanize()

    @property
    def get_team_users(self):
        team_user_ids = list(self.teams.values_list('users__id', flat=True))
        return User.objects.filter(id__in=team_user_ids)

    @property
    def get_team_and_assigned_users(self):
        team_user_ids = list(self.teams.values_list('users__id', flat=True))
        assigned_user_ids = list(self.assigned_to.values_list('id', flat=True))
        user_ids = team_user_ids + assigned_user_ids
        return User.objects.filter(id__in=user_ids)

    class Meta:
        ordering = ['-due_date']



