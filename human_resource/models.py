from django.db import models
from django.contrib.auth.models import User, Group
from admin_site.models import GeneralSettingModel
from admin_site.model_info import *
import barcode
from django.apps import apps
from barcode.writer import ImageWriter
from admin_site.models import DaysModel


def generate_barcode(identifier):
    code = barcode.Code39(identifier, writer=ImageWriter(), add_checksum=False)
    file_name = f'{identifier}'
    file_path = f'media/barcode/staff/{file_name}'
    code.save(file_path)

    return file_path + '.png'


class DepartmentModel(models.Model):
    """"""
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name'],
                name='unique_dept_name_combo'
            )
        ]

    def __str__(self):
        return self.name.upper()

    def number_of_staff(self):
        return StaffModel.objects.filter(department=self).count()


class PositionModel(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(DepartmentModel, on_delete=models.CASCADE, related_name='positions')
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'department'],
                name='unique_dept_name_and_dept_combo'
            )
        ]

    def __str__(self):
        return self.name.upper()

    def number_of_staff(self):
        return StaffModel.objects.filter(position=self).count()


class ThumbPrint(models.Model):
    staff = models.ForeignKey('StaffModel', on_delete=models.CASCADE)
    thumbprint_data = models.BinaryField()

    def __str__(self):
        return self.staff.__str__()


class StaffModel(models.Model):
    """"""
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, null=True, blank=True, default='')
    last_name = models.CharField(max_length=50)

    image = models.FileField(upload_to='images/staff', blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    mobile = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER)

    marital_status = models.CharField(max_length=30, choices=MARITAL_STATUS, null=True, blank=True)
    religion = models.CharField(max_length=30, choices=RELIGION, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    lga = models.CharField(max_length=100, null=True, blank=True)

    department = models.ForeignKey(DepartmentModel, on_delete=models.CASCADE, related_name='department_staffs')
    position = models.ForeignKey(PositionModel, on_delete=models.CASCADE, related_name='position_staffs')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)
    staff_id = models.CharField(max_length=100, blank=True, null=True)
    is_doctor = models.BooleanField(blank=True, default=False)
    employment_date = models.DateField(blank=True, null=True)
    cv = models.FileField(upload_to='staff/cv', null=True, blank=True)

    salary = models.BigIntegerField(blank=True, null=True, default=0)
    bank_name = models.CharField(max_length=100, choices=BANKS, null=True, blank=True)
    account_name = models.CharField(max_length=100, null=True, blank=True)
    account_number = models.CharField(max_length=50, null=True, blank=True)

    blood_group = models.CharField(max_length=20, null=True, choices=BLOOD_GROUP, blank=True)
    genotype = models.CharField(max_length=20, null=True, blank=True, choices=GENOTYPE)
    medical_conditions = models.TextField(null=True, blank=True)

    status = models.CharField(max_length=30, blank=True, default='active')
    barcode = models.FileField(upload_to='barcode/staff', null=True, blank=True)
    thumbprints = models.ManyToManyField(ThumbPrint, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='staff_created_by')

    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        if self.middle_name:
            return "{} {} {}".format(self.first_name, self.middle_name, self.last_name)
        else:
            return "{} {}".format(self.first_name, self.last_name)

    def save(self, *args, **kwargs):
        staff_setting = HRSettingModel.objects.first()

        if staff_setting.auto_generate_staff_id and not self.staff_id:
            last_staff = StaffIDGeneratorModel.objects.filter(status='s').last()
            if last_staff:
                staff_id = str(int(last_staff.last_id) + 1)
            else:
                staff_id = str(1)
            while True:
                gen_id = staff_id
                staff_id = 'stf-' + staff_id.rjust(4, '0')
                staff_exist = StaffModel.objects.filter(staff_id=staff_id).first()
                if not staff_exist:
                    break
                else:
                    staff_id = str(int(gen_id) + 1)
            self.staff_id = staff_id

            generate_id = StaffIDGeneratorModel.objects.create(last_id=gen_id, last_staff_id=self.staff_id, status='f')
            generate_id.save()

        if self.id:
            user_profile = StaffProfileModel.objects.filter(staff=self).first()
            if user_profile:
                user = user_profile.user
                user.email = self.email
                user.save()

                if self.group:
                    self.group.user_set.add(user)

        if self.staff_id and not self.barcode:
            barcode_file_path = generate_barcode(self.staff_id)
            self.barcode = barcode_file_path

        super(StaffModel, self).save(*args, **kwargs)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['staff_id'],
                name='unique_staff_id'
            )
        ]


class StaffIDGeneratorModel(models.Model):
    last_id = models.IntegerField()
    last_staff_id = models.CharField(max_length=100, null=True, blank=True)
    STATUS = (
        ('s', 'SUCCESS'), ('f', 'FAIL')
    )
    status = models.CharField(max_length=10, choices=STATUS, blank=True, default='f')


class StaffProfileModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, related_name='user_staff_profile')
    staff = models.OneToOneField(StaffModel, on_delete=models.CASCADE, null=True, related_name='staff_profile')
    default_password = models.CharField(max_length=100)

    def __str__(self):
        return self.staff.__str__()


class HRSettingModel(models.Model):
    auto_generate_staff_id = models.BooleanField(default=True, blank=True, null=True)


class StaffCertificateModel(models.Model):
    """"""
    staff = models.ForeignKey(StaffModel, on_delete=models.CASCADE, related_name='certificates')
    name = models.CharField(max_length=250)
    certificate = models.FileField(upload_to='document/staff/certificate')
    date_obtained = models.DateField(null=True, blank=True)
    certificate_type = models.CharField(max_length=100, choices=CERTIFICATE_TYPE, blank=True, null=True)

    def __str__(self):
        return "{} ({})".format(self.name, self.certificate_type).upper()


class StaffLeaveModel(models.Model):
    """"""
    staff = models.ForeignKey(StaffModel, on_delete=models.CASCADE, related_name='leaves')
    subject = models.CharField(max_length=250)
    category = models.CharField(max_length=50, choices=LEAVE_CATEGORY)
    start_date = models.DateField()
    end_date = models.DateField()
    duration_count = models.IntegerField()
    duration_type = models.CharField(max_length=30, choices=DURATION_TYPE, default='week')
    approval_status = models.CharField(max_length=30, choices=LEAVE_STATUS, default='pending', blank=True)
    status = models.CharField(max_length=30, choices=ACTIVE_STATUS, default='inactive', blank=True)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)


class ShiftModel(models.Model):
    """"""
    day = models.ForeignKey(DaysModel, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()


class StaffShiftModel(models.Model):
    """"""
    staff = models.ForeignKey(StaffModel, on_delete=models.CASCADE, related_name='shifts')
    shifts = models.ManyToManyField(ShiftModel, blank=True)
