from django.shortcuts import render,HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from .serializers import *
from rest_framework import status
import io
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
# Create your views here.
class RegisterView(APIView):
    def post(self,request):
        serializer = UserSerializers(data = request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            print(serializer.data)
            return Response({"msg":"user registerd successfully"},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class ChangePasswodView(APIView):
    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def post(self,request): 
        self.object = self.get_object()
        serializer = ChangePasswordSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.data.get("password")
        password2 = serializer.data.get("password2")
        if not self.object.check_password(password):
            return Response({"Error":"you entered Wrong old password"},status=status.HTTP_400_BAD_REQUEST)
        self.object.set_password(password2)
        self.object.save()
        return Response({"msg":"user password changed successfully"},status=status.HTTP_200_OK)
            

class SendPasswordResetView(APIView):
    def post(self,request):
        serializer = SendPasswordResetSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({"msg":"password Reset Link send check your email"},status = status.HTTP_200_OK)
        return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)


class UserPasswordResetView(APIView):
    def post(self,request,uid,token):
        serializer = UserPasswordResetSerializer(data = request.data,context = {'uid':uid,'token':token})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password Reset Successfully'},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,format=None):
        serializer = UserProfileViewSerializer(request.user)
        print("data  = ",type(serializer))
        print("data  = ",serializer)
        return Response(serializer.data,status=status.HTTP_200_OK)

class AddAddress(APIView):
    permission_classes = [IsAuthenticated]
    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def post(self,request):
        self.object = self.get_object()
        print("i called")
        serializer = UserAdressSerializer(data = request.data,context={'user':self.object})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"msg":"Address Added successfully"},status=status.HTTP_201_CREATED)
        return Response({"msg":"Address not Added "},status=status.HTTP_400_BAD_REQUEST)
        
class ShowAddress(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,format =None):
            print(request.user)
            data = Address.objects.filter(user = request.user)
            serializer = UserAddressSerializer(data,many=True)
            # serializer.is_valid(raise_exception = True)
            return Response(serializer.data,status=status.HTTP_200_OK)

class UpdatePrimaryAddress(APIView):
    permission_classes = [IsAuthenticated]
    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def post(self,request,format =None):
            self.object = self.get_object()
            serializer = UserUpdatePrimaryAddressSerializer(data = request.data,context={'user':self.object})
            if serializer.is_valid(raise_exception = True):
                return Response({"msg":"Address updated Successfully"},status=status.HTTP_201_CREATED)
            return Response({"msg":"Adress not updated"},status=status.HTTP_400_BAD_REQUEST)

class DeleteAddress(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request,format =None):
            serializer = UserDeleteAddressSerializer(data = request.data)
            if serializer.is_valid(raise_exception = True):
                return Response({"msg":"Address deleted Successfully"},status=status.HTTP_201_CREATED)
            return Response({"msg":"Adress not deleted"},status=status.HTTP_400_BAD_REQUEST)

class UpdateAddress(APIView):
    permission_classes = [IsAuthenticated]
    def put(self,request,format =None,pk=None):
        add = Address.objects.get(id=pk)
        serializers = UserUpdateAddressSerializer(add,data=request.data,partial= True)
        if serializers.is_valid():
            serializers.save()
            return Response({"msg":"Addreess Updated successfully"},status=status.HTTP_200_OK)
        return Response({"err":serializers.errors},status=status.HTTP_400_BAD_REQUEST)