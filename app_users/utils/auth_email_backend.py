from typing import Any
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.base_user import AbstractBaseUser
from django.http import HttpRequest
from app_users.models import CustomUser
from django.db.models import Q


class EmailBackend(ModelBackend):
    def authenticate(self, request, username, password, **kwargs):
        user : CustomUser = None
        try:
            user = CustomUser.objects.get(Q(username = username) | Q(email = username))
            is_password_correct = user.check_password(password)
            is_user_active = self.user_can_authenticate(user)
            if not is_password_correct or is_user_active:
                raise Exception("Wrong password or Inactive")
        
        except:
            return None

        return user
    

    
    def get_user(self, user_id: int):
        user : CustomUser = None
        try:
            user = CustomUser.objects.get(id = user_id)
            if not self.user_can_authenticate(user):
                raise Exception("Inactive")
        except:
            return None
        return user
    