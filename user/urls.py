from django.urls import path

from django.views.decorators.csrf import csrf_exempt
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_simplejwt.views import TokenRefreshView
from .views import UserViewPrivate,CreateUserView,CreateUserView,CustomTokenobtainPairView,LogoutView,AdminView

# https://github.com/rg3915/gallery/blob/master/gallery
urlpatterns = [
     
     path('', csrf_exempt(CreateUserView.as_view())),
     path('token/', CustomTokenobtainPairView.as_view()),
     path('token/refresh/', TokenRefreshView.as_view()),
     path('edite/', UserViewPrivate.as_view()),
     path("logout/", LogoutView.as_view(), name="logout"),
     path("admin/", AdminView.as_view(), name= "user-list"),
     path("admin/<id>/", AdminView.as_view(), name= "user-detail")

]
urlpatterns = format_suffix_patterns(urlpatterns)