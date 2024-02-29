from django.db import models

# Create your models here.


class HomeFirstSliderModel(models.Model):
    heading = models.CharField(max_length=200)
    description = models.TextField()
    button_text = models.CharField(max_length=100)
    LINK = (('homepage', 'HOMEPAGE'), ('about', 'ABOUT'))
    button_link = models.CharField(max_length=30, choices=LINK)
    picture = models.ImageField(upload_to="images/slider")


class OpeningHoursModel(models.Model):
    monday = models.CharField(max_length=100, blank=True, default="8:00am - 5:00pm")
    tuesday = models.CharField(max_length=100, blank=True, default="8:00am - 5:00pm")
    wednesday = models.CharField(max_length=100, blank=True, default="8:00am - 5:00pm")
    thursday = models.CharField(max_length=100, blank=True, default="8:00am - 5:00pm")
    friday = models.CharField(max_length=100, blank=True, default="8:00am - 5:00pm")
    saturday = models.CharField(max_length=100, blank=True, default="8:00am - 5:00pm")
    sunday = models.CharField(max_length=100, blank=True, default="8:00am - 5:00pm")


class ServicesModel(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    picture = models.ImageField(upload_to= 'images/services', null=True, blank=True)


    def __str__(self):
        return "{}".format(self.name).upper()


class TestimonialsModel(models.Model):
    patient_name = models.CharField(max_length=100)
    patient_sickness = models.CharField(max_length=200)
    info = models.TextField()
    picture = models.ImageField(upload_to='images/testimonials')

    def __str__(self):
        return '{}'.format(self.patient_name)


class FAQModel(models.Model):
    question = models.CharField(max_length=400)
    answer = models.TextField()

    def __str__(self):
        return '{}'.format(self.question).upper()


class BlogModel(models.Model):
    title = models.CharField(max_length=300)
    date = models.DateField()
    picture = models.ImageField(upload_to='images/blog')

    def __str__(self):
        return '{}'.format(self.title).upper()


class SiteInfoModel(models.Model):
    site_text = models.TextField()
    site_address = models.CharField(max_length=150)
    site_number = models.CharField(max_length=150)
    site_email = models.EmailField(max_length=150)


class SubscriberModel(models.Model):
    email = models.EmailField()


class IconBoxAboutModel(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    Class = models.CharField(max_length=100, default='fa fa-user-md')

    def __str__(self):
        return '{}'.format(self.name)


class AboutUsModel(models.Model):
    description = models.TextField()
    mission_one = models.CharField(max_length=500)
    mission_two = models.CharField(max_length=500)
    mission_three = models.CharField(max_length=500)
    mission_four = models.CharField(max_length=500)
    mission_five = models.CharField(max_length=500)
    mission_six = models.CharField(max_length=500)
    mission_seven = models.CharField(max_length=500)
    picture = models.ImageField(upload_to='images/about')

    def __str__(self):
        return '{}'.format(self.description)


class DepartmentsModel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    opening_hours_monday = models.CharField(max_length=100, blank=True, default="8:00am - 5:00pm")
    opening_hours_tuesday = models.CharField(max_length=100, blank=True, default="8:00am - 5:00pm")
    opening_hours_wednesday = models.CharField(max_length=100, blank=True, default="8:00am - 5:00pm")
    opening_hours_thursday = models.CharField(max_length=100, blank=True, default="8:00am - 5:00pm")
    opening_hours_friday = models.CharField(max_length=100, blank=True, default="8:00am - 5:00pm")
    opening_hours_saturday = models.CharField(max_length=100, blank=True, default="8:00am - 5:00pm")
    opening_hours_sunday = models.CharField(max_length=100, blank=True, default="8:00am - 5:00pm")
    picture = models.ImageField(upload_to='images/department')
    doctor_image = models.ImageField(upload_to='images/department_doctors')

    def __str__(self):
        return '{}'.format(self.name)


class DoctorsModel(models.Model):
    name = models.CharField(max_length=120)
    position = models.CharField(max_length=100)
    picture = models.ImageField(upload_to='images/doctor')
    facebook_url = models.URLField(null=True, blank=True)
    twitter_url = models.URLField(null=True, blank=True)
    linkedin_url = models.URLField(null=True, blank=True)
    summary = models.TextField()
    degrees = models.CharField(max_length=500, null=True, blank=True)
    address = models.CharField(max_length=300, null=True, blank=True)
    phone_number = models.CharField(max_length=40, null=True, blank=True)
    email_address = models.EmailField(null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.name)


class AppointmentModel(models.Model):
    name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=40)
    email = models.EmailField()
    description = models.TextField()
    date = models.DateTimeField()