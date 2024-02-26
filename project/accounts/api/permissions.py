from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied
from accounts.models import *

class IsVerified(BasePermission):
    def has_permission(self, request, view):
        user_id = view.kwargs.get('user_id', None)
        user = CustomUser.objects.filter(id=user_id).first()
        if not user.is_verified:
            raise PermissionDenied("الحساب غير مؤكد الرجاء تأكيد الحساب والمحاولة من جديد")
        return True
    
class PermissionResetPassword(BasePermission):
    def has_permission(self, request, view):
        user_id = view.kwargs.get('user_id', None)
        code_verification = CodeVerification.objects.filter(user__id=user_id).first()
        print(code_verification.is_verified)
        if not code_verification.is_verified:
            print(code_verification)
            raise PermissionDenied("ليس لديك الصلاحية بتغيير كلمة المرور")
        return True