from HospitalPageAdmin.models import *


def site_info_distributor(request):
    site_info = SiteInfoModel.objects.first()
    blog = BlogModel.objects.all()[:3]
    department_list = DepartmentsModel.objects.all()

    return {
        "site_info": site_info,
        "footer_blog_list": blog,
        "department_list": department_list,
    }
