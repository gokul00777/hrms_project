
from django.shortcuts import render
from .models import CustomUser
from functools import wraps
from django.http import HttpResponseRedirect
def require_user_type(user_type):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            try:
                # Get the current logged-in user
                user = CustomUser.objects.get(id=request.user.id)
                # Check if user has the required user_type
                if str(user.user_type) in str(user_type):
                    return view_func(request, *args, **kwargs)
                else:
                    return render(request,'hr_management/404_not_found.html')
            except:
                return HttpResponseRedirect('/')
        return wrapper
    return decorator



