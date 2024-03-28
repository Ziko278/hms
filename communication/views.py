from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import get_connection, send_mail
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.core import serializers
from django.contrib.messages.views import SuccessMessageMixin, messages
from django.utils.html import strip_tags
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from human_resource.models import StaffModel, StaffProfileModel, DepartmentModel
from communication.models import *
from communication.forms import *
from patient.models import PatientModel


def get_smtp_connection(request):
    communication_setting = CommunicationSettingModel.objects.first()
    if not communication_setting:
        return False
    if not communication_setting.default_smtp:
        return False
    smtp_config = communication_setting.default_smtp
    smtp_connection = get_connection(
        host=smtp_config.host,
        port=smtp_config.port,
        username=smtp_config.username,
        password=smtp_config.password,
        use_tls=True,  # Adjust based on your SMTP configuration
    )
    return smtp_connection, smtp_config.email


def format_whatsapp_number(number):
    return number


class CommunicationDashboardView(LoginRequiredMixin, TemplateView):

    template_name = 'communication/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['department_list'] = DepartmentModel.objects.all().order_by('name')
        context['contact_category_list'] = ContactCategoryModel.objects.all().order_by('name')
        return context


class NoteCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = NoteModel
    form_class = NoteForm
    template_name = 'communication/dashboard.html'
    success_message = 'Note Successfully Added'

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER') or reverse_lazy('admin_dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['note_list'] = NoteModel.objects.all().order_by('name')
        return context


class NoteListView(LoginRequiredMixin, ListView):
    model = NoteModel
    fields = '__all__'
    template_name = 'communication/dashboard.html'
    context_object_name = "note_list"

    def get_queryset(self):
        return NoteModel.objects.all().order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = NoteForm
        return context


class NoteUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = NoteModel
    form_class = NoteForm
    template_name = 'communication/dashboard.html'
    success_message = 'Note Successfully Updated'

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER') or reverse_lazy('admin_dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class NoteDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = NoteModel
    fields = '__all__'
    template_name = 'communication/dashboard.html'
    context_object_name = "note"
    success_message = 'Note Successfully Deleted'

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER') or reverse_lazy('admin_dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ContactCategoryCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = ContactCategoryModel
    permission_required = 'communication.add_contactcategorymodel'
    form_class = ContactCategoryForm
    template_name = 'communication/contact_category/index.html'
    success_message = 'Contact Category Successfully Added'

    def get_success_url(self):
        return reverse('contact_category_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contact_category_list'] = ContactCategoryModel.objects.all().order_by('name')
        return context


class ContactCategoryListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = ContactCategoryModel
    permission_required = 'communication.add_contactcategorymodel'
    fields = '__all__'
    template_name = 'communication/contact_category/index.html'
    context_object_name = "contact_category_list"

    def get_queryset(self):
        return ContactCategoryModel.objects.all().order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ContactCategoryForm
        return context


class ContactCategoryUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = ContactCategoryModel
    permission_required = 'communication.add_contactcategorymodel'
    form_class = ContactCategoryForm
    template_name = 'communication/contact_category/index.html'
    success_message = 'Contact Category Successfully Updated'

    def get_success_url(self):
        return reverse('contact_category_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ContactCategoryDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = ContactCategoryModel
    permission_required = 'communication.add_contactcategorymodel'
    fields = '__all__'
    template_name = 'communication/contact_category/delete.html'
    context_object_name = "contact_category"
    success_message = 'Contact Category Successfully Deleted'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('contact_category_index')


class ContactCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = ContactModel
    permission_required = 'communication.add_contactmodel'
    form_class = ContactForm
    template_name = 'communication/contact/index.html'
    success_message = 'Contact Successfully Added'

    def dispatch(self, *args, **kwargs):
        if self.request.method == 'GET':
            return redirect(reverse('contact_index'))
        return super(ContactCreateView, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse('contact_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class ContactListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = ContactModel
    permission_required = 'communication.add_contactmodel'
    fields = '__all__'
    template_name = 'communication/contact/index.html'
    context_object_name = "contact_list"

    def get_queryset(self):
        return ContactModel.objects.all().order_by('full_name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ContactForm
        context['contact_category_list'] = ContactCategoryModel.objects.all().order_by('name')
        return context


class ContactUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = ContactModel
    permission_required = 'communication.add_contactmodel'
    form_class = ContactForm
    template_name = 'communication/contact/index.html'
    success_message = 'Contact Successfully Updated'

    def dispatch(self, *args, **kwargs):
        if self.request.method == 'GET':
            return redirect(reverse('contact_index'))
        return super(ContactUpdateView, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse('contact_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class ContactDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = ContactModel
    permission_required = 'communication.add_contactmodel'
    fields = '__all__'
    template_name = 'communication/contact/delete.html'
    context_object_name = "contact"
    success_message = 'Contact Successfully Deleted'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('contact_index')


class SMTPConfigurationCreateView(SuccessMessageMixin, CreateView):
    model = SMTPConfigurationModel
    form_class = SMTPConfigurationForm
    success_message = 'Email Configuration Added Successfully'
    template_name = 'communication/smtp_configuration/index.html'

    def dispatch(self, *args, **kwargs):
        if self.request.method == 'GET':
            return redirect(reverse('smtp_configuration_index'))
        return super(SMTPConfigurationCreateView, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse('smtp_configuration_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['smtp_configuration_list'] = SMTPConfigurationModel.objects.all().order_by('name')
        return context


class SMTPConfigurationListView(ListView):
    model = SMTPConfigurationModel
    fields = '__all__'
    template_name = 'communication/smtp_configuration/index.html'
    context_object_name = "smtp_configuration_list"

    def get_queryset(self):
        return SMTPConfigurationModel.objects.all().order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SMTPConfigurationForm

        return context


class SMTPConfigurationUpdateView(SuccessMessageMixin, UpdateView):
    model = SMTPConfigurationModel
    form_class = SMTPConfigurationForm
    success_message = 'Email Configuration Updated Successfully'
    template_name = 'communication/smtp_configuration/index.html'

    def dispatch(self, *args, **kwargs):
        if self.request.method == 'GET':
            return redirect(reverse('smtp_configuration_index'))
        return super(SMTPConfigurationUpdateView, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse('smtp_configuration_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['smtp_configuration_list'] = SMTPConfigurationModel.objects.all().order_by('name')

        return context


class SMTPConfigurationDeleteView(SuccessMessageMixin, DeleteView):
    model = SMTPConfigurationModel
    success_message = 'Email Configuration Deleted Successfully'
    fields = '__all__'
    template_name = 'communication/smtp_configuration/delete.html'
    context_object_name = "smtp_configuration"

    def get_success_url(self):
        return reverse("smtp_configuration_index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class CommunicationSettingCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = CommunicationSettingModel
    form_class = CommunicationSettingForm
    permission_required = 'communication.change_communicationsettingmodel'
    success_message = 'Communication Setting Updated Successfully'
    template_name = 'communication/communication_setting/create.html'

    def dispatch(self, *args, **kwargs):
        communication_setting = CommunicationSettingModel.objects.first()
        if not communication_setting:
            return super(CommunicationSettingCreateView, self).dispatch(*args, **kwargs)
        else:
            return redirect(reverse('communication_setting_edit', kwargs={'pk': communication_setting.pk}))

    def get_success_url(self):
        return reverse('communication_setting_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class CommunicationSettingDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = CommunicationSettingModel
    permission_required = 'communication.change_communicationsettingmodel'
    fields = '__all__'
    template_name = 'communication/communication_setting/detail.html'
    context_object_name = "communication_setting"

    def dispatch(self, *args, **kwargs):
        communication_setting = CommunicationSettingModel.objects.first()
        if communication_setting:
            if self.kwargs.get('pk') != communication_setting.id:
                return redirect(reverse('communication_setting_detail', kwargs={'pk': communication_setting.pk}))
            return super(CommunicationSettingDetailView, self).dispatch(*args, **kwargs)
        else:
            return redirect(reverse('communication_setting_create'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class CommunicationSettingUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = CommunicationSettingModel
    permission_required = 'communication.change_communicationsettingmodel'
    form_class = CommunicationSettingForm
    success_message = 'Communication Setting Updated Successfully'
    template_name = 'communication/communication_setting/create.html'

    def get_success_url(self):
        return reverse('communication_setting_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['communication_setting'] = self.object
        return context


def get_staff_chat(request):
    other_staff_id = request.GET.get('staff_id')
    other_staff = StaffModel.objects.get(pk=other_staff_id)
    staff_profile = StaffProfileModel.objects.get(user=request.user)
    staff = staff_profile.staff
    messages_sent = MessageModel.objects.filter(sender=staff, receiver=other_staff)

    # Filter messages where staff 2 is the sender and staff 1 is the receiver
    messages_received = MessageModel.objects.filter(sender=other_staff, receiver=staff)

    # Combine the two querysets using the | (OR) operator
    message_list = messages_sent | messages_received

    # Order the messages by the creation time
    message_list = message_list.order_by('created_at').reverse()

    context = {
        'message_list': message_list
    }

    return render(request, 'communication/staff_chat.html', context)


def send_chat(request):
    other_staff_id = request.GET.get('staff_id')
    other_staff = StaffModel.objects.get(pk=other_staff_id)
    staff_profile = StaffProfileModel.objects.get(user=request.user)
    staff = staff_profile.staff
    message = request.GET.get('message')

    message = MessageModel.objects.create(sender=staff, receiver=other_staff, message=message)
    message.save()
    if message.id:
        return HttpResponse(True)
    return HttpResponse(False)


def send_email(request):
    email_list = []
    email_string = request.POST.get('email')
    if email_string:
        email_string_list = email_string.split(",")
        for mail in email_string_list:
            if '@' in mail and '.' in mail:
                email_list.append(mail.strip().lower())
    patient = request.POST.get('patient')
    patient_email_list = []
    if patient:
        if patient == 'all':
            patient_email_list = PatientModel.objects.exclude(email=None).values_list('email')
        elif patient == 'male':
            patient_email_list = PatientModel.objects.filter(gender='male').exclude(email=None).values_list('email')
        elif patient == 'female':
            patient_email_list = PatientModel.objects.filter(gender='female').exclude(email=None).values_list('email')
    for email in patient_email_list:
        email_list += email

    staff = request.POST.get('staff')
    staff_email_list = []
    if staff:
        if staff == 'all':
            staff_email_list = StaffModel.objects.exclude(email=None).values_list('email')
        elif staff == 'male':
            staff_email_list = StaffModel.objects.filter(gender='male').exclude(email=None).values_list('email')
        elif staff == 'female':
            staff_email_list = StaffModel.objects.filter(gender='female').exclude(email=None).values_list('email')
        else:
            staff_email_list = StaffModel.objects.filter(department__id=staff).exclude(email=None).values_list('email')
    for email in staff_email_list:
        email_list += email

    contact = request.POST.get('contact')
    contact_email_list = []
    if contact:
        if contact == 'all':
            contact_email_list = ContactModel.objects.exclude(email=None).values_list('email')
        else:
            contact_email_list = ContactModel.objects.filter(category__id=contact).exclude(email=None).values_list('email')
    for email in contact_email_list:
        email_list += email

    if len(email_list) == 0:
        messages.error(request, 'No Valid Email Address Selected or Entered')
        return redirect(reverse('communication_dashboard'))

    subject = request.POST.get('subject')
    body = request.POST.get('body')
    connection = get_smtp_connection(request)
    if connection:
        smtp_connection, sender_email = connection
    else:
        messages.error(request, 'Failed To Establish a Connection, Check Email Setting')
        redirect(reverse('communication_dashboard'))

    context = {
        'domain': get_current_site(request),
        'subject': subject,
        'body': body
    }

    html_message = render_to_string('communication/template/send_mail.html', context)
    plain_message = strip_tags(html_message)

    mail_sent = send_mail(subject, plain_message, sender_email, email_list, html_message=html_message,
                               fail_silently=True, connection=smtp_connection)

    if mail_sent > 0:
        messages.success(request, '{} out of {} Mail(s) sent successfully'.format(mail_sent, len(email_list)))
    else:
        messages.warning(request, 'No mail sent, this may be due to wrong addresses provided or network issues')
    return redirect(reverse('communication_dashboard'))


def send_whatsapp_message(request):
    if request.method == 'POST':
        number_list = []
        number_string = request.POST.get('number')
        if number_string:
            number_string_list = number_string.split(",")
            for number in number_string_list:
                if format_whatsapp_number(number):
                    number_list.append(format_whatsapp_number(number))

        patient = request.POST.get('patient')
        patient_number_list = []
        if patient:
            if patient == 'all':
                patient_number_list = PatientModel.objects.exclude(phone_number=None).values_list('phone_number')
            elif patient == 'male':
                patient_number_list = PatientModel.objects.filter(gender='male').exclude(phone_number=None).values_list('phone_number')
            elif patient == 'female':
                patient_number_list = PatientModel.objects.filter(gender='female').exclude(phone_number=None).values_list('phone_number')

        for number in patient_number_list:
            if format_whatsapp_number(number):
                number_list.append(format_whatsapp_number(number))

        staff = request.POST.get('staff')
        staff_number_list = []
        if staff:
            if staff == 'all':
                staff_number_list = StaffModel.objects.exclude(email=None).values_list('phone_number')
            elif staff == 'male':
                staff_number_list = StaffModel.objects.filter(gender='male').exclude(phone_number=None).values_list('phone_number')
            elif staff == 'female':
                staff_number_list = StaffModel.objects.filter(gender='female').exclude(phone_number=None).values_list('phone_number')
            else:
                staff_number_list = StaffModel.objects.filter(department__id=staff).exclude(phone_number=None).values_list('phone_number')

        for number in staff_number_list:
            if format_whatsapp_number(number):
                number_list.append(format_whatsapp_number(number))

        contact = request.POST.get('contact')
        contact_number_list = []
        if contact:
            if contact == 'all':
                contact_number_list = ContactModel.objects.exclude(phone_number=None).values_list('phone_number')
            else:
                contact_number_list = ContactModel.objects.filter(category__id=contact).exclude(phone_number=None).values_list('phone_number')

        for number in contact_number_list:
            if format_whatsapp_number(number):
                number_list.append(format_whatsapp_number(number))

        if len(number_list) == 0:
            messages.error(request, 'No Valid Phone Number Selected or Entered')
            return redirect(reverse('send_whatsapp_message'))

        subject = request.POST.get('subject')
        body = request.POST.get('body')

        # send whatsapp message

    return render(request, 'communication/whatsapp_dashboard.html')


