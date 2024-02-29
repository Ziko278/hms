from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse

from website.models import *
from website.models import *

# Create your views here.


def home_page_view(request):
    slider_list = HomeFirstSliderModel.objects.all()[:3]
    opening_hours_list = OpeningHoursModel.objects.first()
    service_list = ServicesModel.objects.all()
    testimonial_list = TestimonialsModel.objects.all()
    department_list = DepartmentsModel.objects.all()
    faq_list = FAQModel.objects.all()
    blog_list = BlogModel.objects.all()
    footer_blog_list = BlogModel.objects.all()[:3]
    site_info = SiteInfoModel.objects.first()
    data = {
        'slider_list': slider_list,
        'opening_hours': opening_hours_list,
        'service_list': service_list,
        'testimonial_list': testimonial_list,
        'department_list': department_list,
        'faq_list': faq_list,
        'blog_list': blog_list,
        'site_info': site_info,
    }
    return render(request, 'website/homepage.html', data)


def about_page_view(request):
    service_list = ServicesModel.objects.all()
    testimonial_list = TestimonialsModel.objects.all()[0:2]
    about = IconBoxAboutModel.objects.all()
    about_us = AboutUsModel.objects.first()
    department_list = DepartmentsModel.objects.all()
    doctor_list = DoctorsModel.objects.all()

    partial_testimonial_list = TestimonialsModel.objects.all()[2:10]
    data = {
        'service_list': service_list,
        'testimonial_list': testimonial_list,
        'about': about,
        'about_us': about_us,
        'department_list': department_list,
        'doctor_list': doctor_list,
        'partial_testimonial_list': partial_testimonial_list,
    }
    return render(request, 'website/about.html', data)


def services_page_view(request):
    return render(request, 'website/services.html')


def contact_page_view(request):
    site_info = SiteInfoModel.objects.first()
    opening_hours = OpeningHoursModel.objects.all()

    data = {
        'site_info': site_info,
        'opening_hours': opening_hours,
    }
    return render(request, 'website/contact.html')


def subscriber_view(request):
    if request.method == 'POST':
        form = SubscriberForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Subscription Added Successfully')
            return redirect(reverse('homepage'))
        else:
            messages.error(request, 'Subscription Failed, Try Again!')
            return redirect(reverse('homepage'))
    else:
        pass

    data = {
        'subscriber_form': SubscriberForm
    }

    return render(request, 'website/layout.html', data)


def departments_view(request, pk):
    departments = DepartmentsModel.objects.get(pk=pk)
    department_list = DepartmentsModel.objects.all()
    site_info = SiteInfoModel.objects.first()
    opening_hours = OpeningHoursModel.objects.all()

    data = {
        'departments': departments,
        'department_list': department_list,
        'site_info': site_info,
        'opening_hours': opening_hours,
    }

    return render(request, 'website/departments.html', data)


def appointment_view(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        form.cleaned_data.get('message')
        if form.is_valid():
            appointment = form.save()
            if appointment.id:
                description = form.cleaned_data.get('description')
                date = form.cleaned_data.get('date')
                email = form.cleaned_data.get('email')
                message = """{}
                
                            {}""".format(description, date)
                mail_sent = send_mail(subject='Appointment Alert!', message=message, from_email=email )

    else:
        messages.error(request, 'Appointment Not Sent, Try Again!')


    data = {
        'appointment_form': AppointmentForm,
    }

    return render(request, 'website/homepage.html', data)


def doctors_details_view(request, pk):
    doctors_list = DoctorsModel.objects.get(pk=pk)
    opening_hours = OpeningHoursModel.objects.first()
    site_info = SiteInfoModel.objects.first()

    data = {
        'doctors_list': doctors_list,
        'opening_hours': opening_hours,
        'site_info': site_info,
    }

    return render(request, 'website/doctors.html', data)


def our_team_view(request):
    doctors_list = DoctorsModel.objects.all()

    data = {
        'doctors_list': doctors_list,
    }

    return render(request, 'website/team.html', data)