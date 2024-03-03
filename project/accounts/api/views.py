from django.shortcuts import render
from rest_framework.generics import *
from rest_framework.views import APIView
from rest_framework.permissions import *
from .serializer import *
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from accounts.utils import Utlil
from accounts.methodes import *
from .permissions import *

# End Points for SignUp User
class SignUpView(APIView):
    def post(self, request):
        user_information = request.data
        serializer = SignUpSerializer(data=user_information)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = CustomUser.objects.get(email=user_data['email'])
        code = generate_code()
        email_body = 'Hi '+user.username+' Use the code below to verify your email \n'+ str(code)
        data= {'to_email':user.email, 'email_subject':'Verify your email','username':user.username, 'code': str(code)}
        Utlil.send_email(data)
        code_verivecation = CodeVerification.objects.create(user=user, code=code)
        token = RefreshToken.for_user(user)
        tokens = {
            'refresh':str(token),
            'accsess':str(token.access_token)
        }
        return Response({'information_user':user_data,'tokens':tokens})

# End Points for Login User
class UserLoginApiView(APIView):
    # serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        user = CustomUser.objects.get(email = request.data['username'])
        token = RefreshToken.for_user(user)
        data = serializer.data
        data['image'] = request.build_absolute_uri(user.image.url)
        data['tokens'] = {'refresh':str(token), 'access':str(token.access_token)}
        return Response(data, status=status.HTTP_200_OK)

# End Points for Logout User
class LogoutAPIView(APIView):
    serializer_class = UserLogoutSerializer
    permission_classes = [IsAuthenticated, IsVerified]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

# End Points For Verified Account
class VerifyAccount(APIView):
    permission_classes = [HaveCodeVerifecation,]

    def get_permissions(self):
        self.request.pk = self.kwargs.get('pk') # Pass the pk to the request
        return super().get_permissions()
    
    def put(self, request, pk):
        code = request.data['code']
        user = CustomUser.objects.get(pk=pk)
        code_ver = CodeVerification.objects.filter(user=user.id).first()
        if code_ver:
            if str(code) == str(code_ver.code):
                if timezone.now() > code_ver.expires_at:
                    return Response({"message":"Verification code has expired"}, status=status.HTTP_400_BAD_REQUEST)
                user.is_verified = True
                user.save()
                code_ver.delete()
                return Response({"message":'verification account hass been seccessfuly', 'user_id':user.id},status=status.HTTP_200_OK)
            else:
                return Response({'message':'الرمز خاطئ, يرجى إعادة إدخال الرمز بشكل صحيح'})

# End Points For Get Code To Reset Password
class GetCodeResetPassword(APIView):

    def get_permissions(self):
        self.request.pk = self.kwargs.get('pk') # Pass the pk to the request
        return super().get_permissions()
    
    def post(self, request):
        email = request.data['email']
        try: 
            user = get_object_or_404(CustomUser, email=email)
            # existing_code = CodeVerification.objects.filter(user=user).first()
            # if existing_code:
            #     existing_code.delete()
            code_verivecation = generate_code()
            data= {'to_email':user.email, 'email_subject':'Verify your email','username':user.username, 'code': str(code_verivecation)}
            Utlil.send_email(data)
            code = CodeVerification.objects.create(user=user, code=code_verivecation)
            return Response({'message':'تم ارسال رمز التحقق',
                             'user_id' : user.id})
        except:
            raise serializers.ValidationError({'error':'pleace enter valid email'})
    
# End Points For Verified Account To Reset Password
class VerifyCodeToChangePassword(APIView):
    permission_classes = [ IsVerified, HaveCodeVerifecation, ]

    def get_permissions(self):
        self.request.pk = self.kwargs.get('pk') # Pass the pk to the request
        return super().get_permissions()
    
    def post(self, request, pk):
        code = request.data['code']
        user = CustomUser.objects.get(id=pk)
        code_ver = CodeVerification.objects.filter(user=user.id).first()
        if code_ver:
            if str(code) == str(code_ver.code):
                if timezone.now() > code_ver.expires_at:
                    return Response({"message":"Verification code has expired"}, status=status.HTTP_400_BAD_REQUEST)
                code_ver.is_verified = True
                code_ver.save()
                return Response({"message":"تم التحقق من الرمز", 'user_id':code_ver.user.id},status=status.HTTP_200_OK)
            else:
                return Response({'message':'الرمز خاطئ, يرجى إعادة إدخال الرمز بشكل صحيح'})
        
# End Points For Reset Password
class ResetPasswordView(UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = ResetPasswordSerializer
    permission_classes = [AllowAny, IsVerified, HaveCodeVerifecation, PermissionResetPassword]

    def get_permissions(self):
        self.request.pk = self.kwargs.get('pk')
        return super().get_permissions()
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['pk']=self.kwargs.get('pk')
        return context

    # def get_queryset(self):
    #     pk = self.kwargs.get('pk')
    #     user = CustomUser.objects.get(id=pk)
    #     return self.get_serializer(user, many=False)
    
    # def put(self, request, pk):
    #     user = CustomUser.objects.get(pk=pk)
    #     try :
    #         code = CodeVerification.objects.filter(user=user).first()
    #         serializer = self.get_serializer(data=request.data)
    #         serializer.is_valid(raise_exception=True)
    #         serializer.save()
    #         code.delete()
    #         messages = {
    #             'message':'تم تغيير كلمة المرور بنجاح'
    #         }
    #         return Response(messages, status=status.HTTP_200_OK)
    #     except:
    #         return Response("ليس لديك الصلاحية بتغيير كلمة المرور")

# End Points For Update Image     
class UpdateImageUserView(UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UpdateUserSerializer
    permission_classes = [IsAuthenticated, IsVerified]

    def get_object(self):
        pk = self.kwargs.get('pk')
        return self.get_queryset().get(pk=pk)

# End Point For List Information User
class ListInformationUserView(RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsVerified]
    queryset = CustomUser.objects.all()
    serializer_class= CustomUserSerializer
