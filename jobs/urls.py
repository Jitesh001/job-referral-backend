from django.urls import path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView

from . import apis

app_name = "jobs"

router = routers.DefaultRouter()
router.register("user/jobs", apis.UserJobsViewSet)

urlpatterns = [
    path("api/auth/register/", apis.RegisterView.as_view(), name="register"),
    path("api/auth/request-otp/", apis.RequestOTPView.as_view(), name="request_otp"),
    path("api/auth/verify-otp/", apis.VerifyOTPView.as_view(), name="verify_otp"),
    path("api/user/profile/", apis.UserProfileView.as_view(), name="user_profile"),
    path("api/user/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path(
        "api/all-job-list/",
        apis.JobPostListAPIView.as_view(),
        name="all_job_list",
    ),
]

urlpatterns += router.urls
