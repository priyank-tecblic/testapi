from rest_framework import serializers
from .models import *
import django.contrib.auth.password_validation as validators
from django.core.exceptions import ValidationError
from django.utils.encoding import smart_str,force_bytes,DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from .utils import Util
class UserSerializers(serializers.ModelSerializer):
    # password2 = serializers.CharField(style={'input':"password"},write_only=True)
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    class Meta:
        model = User
        fields = ['id','name','email','password','password2']
        extra_kwargs = {
            'password':{'write_only':True}
        }
    def validate(self, attrs):
        password = attrs.get("password")
        password2 = attrs.get("password2")
        print("first")
        if password != password2:
            raise serializers.ValidationError({"msg":"passwords and confirm passwords aren't match"})
        return attrs

    def create(self,validated_data):
        password = validated_data.pop('password',None)
        passwor2 = validated_data.pop('password2',None)
        print("second")
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        print("instance=",instance)
        return instance

class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField()
    password2 = serializers.CharField()
    class Meta:
        fields = ['password','password2']

class SendPasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        fields = ['email']
    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            print("uid=",uid)
            token = PasswordResetTokenGenerator().make_token(user)
            print("Password Reset token = ",token)
            link = "http://localhost:8000/api/reset-password/"+uid+'/'+token+'/'
            print("Password Reset link = ",link)
            data = {
                'subject':"Reset your password",
                'body':f'click Following Link for Reset your Password {link}',
                'to_email':user.email
            }
            Util.send_email(data)
        else:
            raise serializers.ValidationError('you are not a register user')
        return attrs

class UserPasswordResetSerializer(serializers.Serializer):
    
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    class Meta:
        fields = ['password','password2']
    def validate(self, attrs):
        try:
            password = attrs.get("password")
            password2 = attrs.get("password2")
            uid = self.context.get('uid')
            token = self.context.get('token')
            id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id= id)
            if not PasswordResetTokenGenerator().check_token(user,token):
                raise ValidationError('Token is not valid or Expired')
            if password!=password2:
                raise serializers.ValidationError('Passwords and confirm passwords are not match')
            user.set_password(password)
            user.save()
            return super().validate(attrs)
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user,token)
            raise ValidationError('Token is not valid or Expired')

class UserProfileViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email','name']

class UserAdressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['street','area','pincode','primary']

    def create(self,validated_data):
        print("i called")
        user = self.context.get('user')
        primary = validated_data.pop('primary',None)
        print("User = ",user)
        if Address.objects.filter(primary = True,user = user).first() is not None and primary == True:
            raise serializers.ValidationError({"error":"your address can't be added because you write primary is True"})
        instance = self.Meta.model(**validated_data)
        instance.user = user
        instance.primary = primary
        instance.save()
        print("instance=",instance)
        return instance
class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id','street','primary','area','pincode']

class UserUpdatePrimaryAddressSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    class Meta:
        model = Address
        fields = ['id']
    def validate(self, attrs):
        id = attrs.get('id')
        print("id = ",id)
        Address.objects.filter(primary=True,user = self.context.get("user")).update(primary=False)
        Address.objects.filter(id = id).update(primary = True)
        return attrs

class UserDeleteAddressSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    class Meta:
        model = Address
        fields = ['id']
    def validate(self, attrs):
        id = attrs.get('id')
        print("id = ",id)
        Address.objects.filter(id = id).delete()
        if Address.objects.first() is not None:
            add = Address.objects.first()
            add.primary = True
            add.save()
        return attrs

class UserUpdateAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"
    
    def update(self, instance, validated_data,pk = None):
        instance.area = validated_data.get("area",instance.area)
        instance.street = validated_data.get("street",instance.street)
        instance.save()    
        return instance