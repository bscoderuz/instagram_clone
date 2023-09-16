from django.utils.datetime_safe import datetime
from rest_framework import permissions
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import DONE, CODE_VERIFIED, NEW, VIA_EMAIL, VIA_PHONE

from .models import User
from .serializers import SignUpSerializer, ChangeUserInformation
from apps.shared.utility import send_email


class CreateUserView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = SignUpSerializer


class VerifyAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, *args, **kwargs):
        user = self.request.user
        code = self.request.data.get('code')

        self.check_verify(user, code)
        return Response(
            data={
                'success': True,
                'auth_satus': user.auth_status,
                'access': user.token()['access'],
                'refresh': user.token()['refresh_token']
            }
        )

    @staticmethod
    def check_verify(user, code):
        verifies = user.verify_codes.filter(expiration_time__gte=datetime.now(), code=code, is_confirmed=False)
        if not verifies.exists():
            data = {
                'message': "Tasdiqlash kodingiz xato yoki eskirgan!"
            }
            raise ValidationError(data)
        else:
            verifies.update(is_confirmed=True)
        if user.auth_status == NEW:
            user.auth_status = CODE_VERIFIED
            user.save()
        return True


class GetNewVerification(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = self.request.user
        self.check_verification(user)
        if user.auth_type == VIA_EMAIL:
            code = user.create_verify_code(VIA_EMAIL)
            send_email(user, code)
        elif user.auth_type == VIA_PHONE:
            code = user.create_verify_code(VIA_PHONE)
            send_email(user, code)
        else:
            data = {
                'message': "Email yoki telefon raqami noto'g'ri!"
            }
            raise ValidationError(data)
        return Response(
            {
                'success': True,
                'message': "Tasdiqlash kodingiz qayta yuborildi."
            }
        )

    @staticmethod
    def check_verification(user):
        verifies = user.verify_codes.filter(expiration_time__gte=datetime.now(), is_confirmed=False)
        if verifies.exists():
            data = {
                'message': "Kodingiz hali ishlatish uchun yaroqli, Biroz kutib turing!"
            }
            raise ValidationError(data)


class ChangeUserInformationAPIView(UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangeUserInformation
    http_method_names = ['patch', 'put']

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        super(ChangeUserInformationAPIView, self).update(request, *args, **kwargs)
        data = {
            'success': True,
            'message': "User updated successfully",
            'auth_status': self.request.user.auth_status
        }
        return Response(data, status=200)

    def partial_update(self, request, *args, **kwargs):
        super(ChangeUserInformationAPIView, self).update(request, *args, **kwargs)
        data = {
            'success': True,
            'message': "User updated successfully",
            'auth_status': self.request.user.auth_status
        }
        return Response(data, status=200)
