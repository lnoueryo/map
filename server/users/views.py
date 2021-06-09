from django.shortcuts import render, get_object_or_404
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import NewUser
from .serializers import RegisterUserSerializer, UserSerializer
from django.http import JsonResponse
from rest_framework.throttling import UserRateThrottle

import urllib.request, json
import urllib.parse
import datetime
# import 

class CustomUserCreate(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        reg_serializer = RegisterUserSerializer(data=request.data)
        if reg_serializer.is_valid():
            newuser = reg_serializer.save()
            if newuser:
                # raise serializers.ValidationError('練習')
                refresh = RefreshToken.for_user(newuser)
                jwt = ({
                    'access': str(refresh.access_token),
                })
                return Response(jwt, status=status.HTTP_201_CREATED)
        return Response(reg_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomUserAPI(APIView):
    permission_classes = [IsAuthenticated]
    # authentication_classes = (authentication.TokenAuthentication,)
    # permission_classes = (permissions.IsAdminUser,)

    # def get_object(self, pk):
    #     user = get_object_or_404(NewUser, pk=pk)
    #     return user

    # def get(self, request, pk):
    #     user = self.get_object(pk)
    #     # user = self.get_object(pk)
    #     serializer = UserSerializer(user)
    #     return Response(serializer.data)
    def get(self, request):
        users = NewUser.objects.all()
        serializer = UserSerializer(users, many=True)

        return JsonResponse(serializer.data, safe=False)
        # return serializer.data

    def put(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = self.get_object(pk=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# class CustomUserAPI(generics.ListCreateAPIView):
#     permission_classes = [IsAuthenticated]
#     queryset = NewUser.objects.all()
#     serializer_class = UserSerializer
