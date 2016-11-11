from django.conf.urls import url, include
from accounts.views import RegistrationView
from accounts.forms import RegistrationForm

from . import views

app_name = 'accounts'
urlpatterns = [
    url(r'^register/$',
        RegistrationView.as_view(
            form_class=RegistrationForm
        ), name='registration_register'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^', include('registration.backends.hmac.urls')),
]
