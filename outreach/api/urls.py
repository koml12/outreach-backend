from rest_framework import routers
from api.views import EvalRegister, SignupIntoEvent, CandidateViewSet, GetAuthToken
from django.urls import path

router = routers.SimpleRouter()

urlpatterns = [
    path("register/evaluator/", EvalRegister.as_view(), name="EvalRegister"),
    path("register/<int:event>/", SignupIntoEvent.as_view(), name="EvalRegister"),
    path("login/", GetAuthToken.as_view())
]

router.register("candidates",CandidateViewSet)

urlpatterns = urlpatterns + router.urls