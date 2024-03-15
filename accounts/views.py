from rest_framework.generics import *
from rest_framework.views import APIView
from rest_framework.permissions import *
from .serializers import *
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from utils.email import Util
from .methodes import *
from .permissions import *



##### sign-up users #####
class SignUpView(APIView):
    def post(self, request):
        user_information = request.data
        serializer = SignUpSerializer(data=user_information)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        user_data = serializer.data
        user = CustomUser.objects.get(email=user_data['email'])
        code = generate_code()
        # email_body = 'Hi '+user.username+' Use the code below to verify your email \n'+ str(code)
        # data= {'to_email':user.email, 'email_subject':'Verify your email','username':user.username, 'code': str(code)}
        # Util.send_email(data)
        CodeVerification.objects.create(user=user, code=code) ## generate code for user
        token = RefreshToken.for_user(user)
        tokens = {
            'refresh':str(token),
            'accsess':str(token.access_token)
        }
        return Response({'information_user':user_data,'tokens':tokens})




##### log-in user #####
class UserLoginApiView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        user = CustomUser.objects.get(email = request.data['username'])
        token = RefreshToken.for_user(user)
        data = serializer.data
        data['image'] = request.build_absolute_uri(user.image.url)
        data['tokens'] = {'refresh':str(token), 'access':str(token.access_token)}
        return Response(data, status=status.HTTP_200_OK)



#### log-out user #####
class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated, IsVerified]
    def post(self, request):
        serializer = UserLogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


##### verify account with generated code #####
class VerifyAccount(APIView):
    permission_classes = [HaveCodeVerifecation,]

    def put(self, request, pk):
        code = request.data['code']
        user = CustomUser.objects.get(id=pk)
        code_ver = CodeVerification.objects.filter(user=user.id).first()
        if code_ver:
            if str(code) == str(code_ver.code):
                if timezone.now() > code_ver.expires_at:
                    return Response({"message":"لقد انتهت صلاحية كود التحقق"}, status=status.HTTP_400_BAD_REQUEST)
                user.is_verified = True
                user.save()
                code_ver.delete()
                return Response({"message":'تمت عملية التحقق بنجاح', 'user_id':user.id},status=status.HTTP_200_OK)
            else:
                return Response({'message':'الرمز خاطئ, يرجى إعادة إدخال الرمز بشكل صحيح'})

##### Reset Password for user ######
class GetCodeResetPassword(APIView):
    def post(self, request):
        email = request.data['email']
        try: 
            user = get_object_or_404(CustomUser, email=email)
            existing_code = CodeVerification.objects.filter(user=user).first()
            if existing_code:
                existing_code.delete()
            code_verivecation = generate_code()
            data= {'to_email':user.email, 'email_subject':'Verify your email','username':user.username, 'code': str(code_verivecation)}
            Util.send_email(data)
            code = CodeVerification.objects.create(user=user, code=code_verivecation)
            return Response({'message':'تم ارسال رمز التحقق',
                             'user_id' : user.id})
        except:
            raise serializers.ValidationError({'error':'pleace enter valid email'})
    


# End Points For Verified Account To Reset Password
class VerifyCodeToChangePassword(APIView):
    permission_classes = [HaveCodeVerifecation, IsVerified, ]

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
    


##### get user profile information #####
class ListInformationUserView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.all()
    serializer_class= CustomUserSerializer




class UserAccount(ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
