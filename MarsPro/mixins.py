from django.shortcuts import redirect
from django.contrib import messages

class LoginRequiredMixin():

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.warning(request, "Siz tizimga kirgansiz !")
            return redirect('user:index')
        return super().dispatch(request, *args, **kwargs)