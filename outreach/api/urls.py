from rest_framework import routers
from api.views import GroupViewSet, QuestionViewSet, QuestionAnswerViewSet, QuestionnaireViewSet, SurveyViewSet, RegistrationViewSet, EvaluatorViewSet, CandidateViewSet, EventViewSet, GetAuthToken
from django.urls import path
from drf_yasg.views import get_schema_view 
from drf_yasg import openapi 
from rest_framework import permissions

router = routers.SimpleRouter()

schema_view = get_schema_view( 
   openapi.Info( 
      title="OutReach API", 
      default_version='v1' 
   ), 
   public=True, 
   permission_classes=(permissions.AllowAny,), 
)

urlpatterns = [
    path("login/", GetAuthToken.as_view()),
    path("docs/", schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

router.register("question",QuestionViewSet)
router.register("group", GroupViewSet, basename="group")
router.register("answer",QuestionAnswerViewSet)
router.register("questionnaire", QuestionnaireViewSet)
router.register("survey", SurveyViewSet)
router.register("candidates", CandidateViewSet)
router.register("evaluators", EvaluatorViewSet)
router.register("registration", RegistrationViewSet)
router.register("event", EventViewSet)


urlpatterns = urlpatterns + router.urls