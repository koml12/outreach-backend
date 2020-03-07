from rest_framework import routers
from api.views import EvalRegister, SignupIntoEvent, CandidateViewSet
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

router = routers.SimpleRouter()

urlpatterns = [
    path("register/evaluator/", EvalRegister.as_view(), name="EvalRegister"),
    path("register/<int:event>/", SignupIntoEvent.as_view(), name="EvalRegister"),
    path("login/", obtain_auth_token)
]

router.register("candidates",CandidateViewSet)

urlpatterns = urlpatterns + router.urls