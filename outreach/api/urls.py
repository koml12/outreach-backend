from rest_framework import routers
from api.views import SMSNotify, divideGroups, GroupViewSet, QuestionViewSet, QuestionAnswerViewSet, QuestionnaireViewSet, SurveyViewSet, RegistrationViewSet, EvaluatorViewSet, CandidateViewSet, EventViewSet, ResumeViewSet, JobViewSet, GetAuthToken
from django.urls import path, include
from drf_yasg.views import get_schema_view 
from drf_yasg import openapi 
from rest_framework import permissions
from django.conf import settings
from django.conf.urls.static import static

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
   path("divideGroups/<int:eventID>", divideGroups),
   path("smsnotify/<int:candidate>", SMSNotify),
   path("docs/", schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui')
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
router.register("resume", ResumeViewSet)
router.register("job", JobViewSet)

urlpatterns = urlpatterns + router.urls
#if settings.DEBUG:
#   urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)