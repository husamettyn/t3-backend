from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.conf import settings

def admin_required(function=None, redirect_field_name=None, login_url=None):
    """
    Decorator for views that checks that the user is logged in and is an admin.
    """
    def check_admin(user):
        if not user.is_authenticated:
            return False # Or raise PermissionDenied? Redirect handled below.
        if not user.is_admin:
            # Optionally raise PermissionDenied or redirect to a specific 'unauthorized' page
            # For now, we just return False, letting user_passes_test handle redirect
            return False
        return True

    actual_decorator = user_passes_test(
        check_admin,
        login_url=login_url or settings.LOGIN_URL, # Use LOGIN_URL from settings
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

# Example Mixin (Optional, can be added later if needed for Class-Based Views)
# from django.contrib.auth.mixins import AccessMixin
#
# class AdminRequiredMixin(AccessMixin):
#     """Verify that the current user is authenticated and is an admin."""
#     def dispatch(self, request, *args, **kwargs):
#         if not request.user.is_authenticated or not request.user.is_admin:
#             return self.handle_no_permission()
#         return super().dispatch(request, *args, **kwargs)