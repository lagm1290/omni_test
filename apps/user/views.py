from django.shortcuts import render
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action
from functools import reduce
import operator
from datetime import datetime, date
from apps.user.forms import PasswordChangeForm
from apps.user.models import User
from apps.user.serializer import UserSerializer

@permission_classes([AllowAny])
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return  super(UserViewSet,self).update(request,*args,**kwargs)

    def get_queryset(self):
        list_q = self.request.GET.get('query', '')
        queryset = self.queryset

        fields_look = [
            'identity__icontains',
            'first_name__icontains',
            'last_name__icontains',
            'email__icontains'
        ]
        for query_term in list_q:
            on_queries = [Q(**{field_look: query_term})
                          for field_look in fields_look]
            queryset = queryset.filter(reduce(operator.or_, on_queries))

        return queryset

    @action(detail=False, methods=['post'], url_path='logout', permission_classes=[IsAuthenticated])
    def logout(self, request):
        request.user.auth_token.delete()
        return Response({"message": "The user has been logged out"},status=status.HTTP_200_OK)


class AuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        user.last_login = datetime.now()
        user.save()

        response = {
            'token': token.key,
            'name': token.user.get_full_name()
        }
        return Response(response, status.HTTP_200_OK)

def activate_user_account(request, uidb64=None, token=None):
    try:
        uid = urlsafe_base64_decode(uidb64)
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    token_generator = PasswordResetTokenGenerator()
    is_valid = token_generator.check_token(user, token)
    if user is not None and is_valid:
        form = PasswordChangeForm(initial={'username': urlsafe_base64_encode(force_bytes(user.pk))})
        return render(request, 'registration/password_reset_comfirm_1.html', {'form': form})

    else:
        return HttpResponse('Activation link is invalid!')

def change_password(request):
    if request.method == 'POST':

        form = PasswordChangeForm(request.POST,request.user)
        if form.is_valid():
            uid=urlsafe_base64_decode(form.cleaned_data['username']).decode()
            user = User.objects.get(pk=uid)
            new_password = form.cleaned_data['rpassword']
            user.set_password(new_password)
            user.is_active = True
            user.save()
            update_session_auth_hash(request, user)
            form = PasswordChangeForm(request.user)
            return render(request, 'registration/password_reset_done.html', {
                'form': form
            })
        else:
            return render(request, 'registration/password_reset_comfirm_1.html', {'form': form})
    else:
        form = PasswordChangeForm(request.user)
        return render(request, 'registration/password_reset_done.html', {
        'form': form
    })


