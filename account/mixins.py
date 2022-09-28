from django.contrib.auth.mixins import AccessMixin
from typing import Any
from account.models import User
# Create your views here.
class RoleRequiredMixin(AccessMixin):
    # PERMISSION_MAPPING = {
    #     User.UserRole.BASE: ['patient.view_patient', 'medicine.view_medicine', ''],
    # }    
    roles_required = None
    login_url: Any = '/login'
    permission_denied_message: str = 'Sorry this page is not authorized for your account'
    @property
    def role(self):
        return self.__role
    @role.setter
    def role(self, val):
        if any(role in User.UserRole.choices for role in val):
            self.__role == val
            # self.permission_required = self.PERMISSION_MAPPING[self.__role]
        else:
            raise ValueError('Role must be in user roles include: base, admin, doctor, assistant')
    def get_roles_required(self):
        return self.roles_required

    def has_role(self):
        """
        Override this method to customize the way permissions are checked.
        """
        roles = self.get_roles_required()
        user_role = self.request.user.role
        print('username: ' + self.request.user.username)
        print('user role ' + user_role)
        print('required role ' + str(roles))
        return user_role in roles \
            or ( user_role in [User.UserRole.ASSISTANT, User.UserRole.DOCTOR ] and User.UserRole.BASE in roles)

    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_role():
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
