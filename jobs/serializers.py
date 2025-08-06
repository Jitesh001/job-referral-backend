from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.validators import validate_email
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import JobPost, User
from .tasks import send_otp_email


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "uuid",
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "is_verified",
        )


class RegisterSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    class Meta:
        model = User
        fields = (
            "phone_number",
            "email",
            "first_name",
            "last_name",
        )

    def validate_email(self, value):
        value = value.lower()
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email already exists.")
        return value

    def validate_phone(self, value):
        value = value.lower()
        if User.objects.filter(phone=value).exists():
            raise serializers.ValidationError("User with this phone already exists.")
        return value

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            phone_number=validated_data.get("phone_number"),
        )
        user.save()
        return user

    def create_otp(self, user):
        otp = user.generate_otp()
        send_otp_email.delay(user.uuid, otp)
        return otp


class VerifyOTPSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    otp = serializers.CharField(required=True)

    def validate(self, attrs):
        username = attrs.get("username").lower()
        is_email = False
        try:
            validate_email(username)
            is_email = True
        except DjangoValidationError:
            is_email = False

        if is_email:
            if not User.objects.filter(email=username).exists():
                raise serializers.ValidationError("Enter valid username")
            attrs["user"] = User.objects.get(email=username)
        else:
            if not User.objects.filter(phone_number=username).exists():
                raise serializers.ValidationError("Enter valid username")
            attrs["user"] = User.objects.get(phone_number=username)

        return attrs

    def verify_otp(self):
        user = self.validated_data["user"]
        otp = self.validated_data["otp"]
        if user.verify_otp(otp):
            if not user.is_verified:
                user.is_verified = True
                user.save()

            # Generate tokens
            refresh = RefreshToken.for_user(user)

            self.validated_data["refresh"] = str(refresh)
            self.validated_data["access"] = str(refresh.access_token)
            return self.validated_data
        raise serializers.ValidationError("OTP is invalid or expired.")


class RequestOTPSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)

    def validate(self, attrs):
        username = attrs.get("username").lower()
        is_email = False
        try:
            validate_email(username)
            is_email = True
        except DjangoValidationError:
            is_email = False

        if is_email:
            if not User.objects.filter(email=username).exists():
                raise serializers.ValidationError("Enter valid username")
            attrs["user"] = User.objects.get(email=username)
        else:
            if not User.objects.filter(phone_number=username).exists():
                raise serializers.ValidationError("Enter valid username")
            attrs["user"] = User.objects.get(phone_number=username)

        return attrs

    def send_otp(self, user):
        otp = user.generate_otp()
        send_otp_email.delay(user.uuid, otp)
        return otp


class JobPostsSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.full_name")

    class Meta:
        model = JobPost
        fields = [
            "uuid",
            "user_name",
            "created",
            "job_title",
            "company_link",
            "company_name",
            "job_location",
            "job_mode",
            "contact_phones",
            "contact_emails",
            "job_description",
        ]


class JobPostDetailSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field="uuid",
        queryset=User.objects.all(),
    )

    class Meta:
        model = JobPost
        fields = [
            "user",
            "job_title",
            "company_link",
            "company_name",
            "job_location",
            "job_mode",
            "contact_phones",
            "contact_emails",
            "job_description",
        ]
