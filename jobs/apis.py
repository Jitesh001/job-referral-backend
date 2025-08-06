from rest_framework import generics, permissions, status
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from backend.pagination import PageNumberPagination

from . import serializers
from .filters import JobPostFilter
from .mixins import ABSViewSet, ListDetailViewSet
from .models import JobPost


class UserProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.UserSerializer

    def get_object(self):
        return self.request.user


class RegisterView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = serializers.RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        otp = serializer.create_otp(user)
        return Response(
            {"otp": otp, "user_uuid": user.uuid},
            status=status.HTTP_201_CREATED,
        )


class RequestOTPView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = serializers.RequestOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        otp = serializer.send_otp(user)
        return Response(
            {"otp": otp},
            status=status.HTTP_200_OK,
        )


class VerifyOTPView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = serializers.VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.verify_otp()
        return Response(
            {
                "access": validated_data["access"],
                "refresh": validated_data["refresh"],
                "uuid": validated_data["user"].uuid,
            },
            status=status.HTTP_200_OK,
        )


class JobPostListAPIView(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.JobPostsSerializer
    queryset = JobPost.objects.all()
    pagination_class = PageNumberPagination
    filterset_class = JobPostFilter

    def get_queryset(self):
        return JobPost.objects.exclude(user=self.request.user).order_by("-created")


class UserJobsViewSet(ListDetailViewSet, ABSViewSet):
    serializer_class = serializers.JobPostsSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = JobPost.objects.all()
    pagination_class = PageNumberPagination
    lookup_field = "uuid"

    def get_queryset(self):
        return JobPost.objects.filter(user=self.request.user).order_by("-created")

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data["user"] = request.user.uuid
        serializer = serializers.JobPostDetailSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        try:
            job_post = self.get_object()
        except Exception as exc:
            raise NotFound("Job not found.") from exc

        if job_post.user != request.user:
            raise PermissionDenied(
                "You do not have permission to delete this job post."
            )

        job_post.delete()
        return Response(
            {"detail": "Job deleted successfully."}, status=status.HTTP_204_NO_CONTENT
        )

    def update(self, request, *args, **kwargs):
        try:
            job_post = self.get_object()
        except Exception as exc:
            raise NotFound("Job not found.") from exc

        if job_post.user != request.user:
            raise PermissionDenied("You do not have permission to edit this job post.")

        partial = kwargs.get("partial", False)
        serializer = self.get_serializer(job_post, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_200_OK)
