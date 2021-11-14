from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from spodaily_api import views
from spodaily_api.views import DeleteActivityView, AddFutureActivityView, ExerciseGuideView, \
    MuscleView, \
    RoutineView, RulesOfUseView, AccountView, PastSessionView, RegisterView, UpdateActivityView, Home, \
    RegisterSuccessView, AddContactView, AddPastActivityView, DuplicateProgramSessionView, DeletePastSessionView, \
    DeleteFutureSessionView, DeleteProgramSessionView, MarkSessionAsDone, DeleteFutureActivityView, \
    DeleteProgramActivityView, AddProgramActivityView, UpdateFutureActivityView, UpdateProgramActivityView, FoodHome, CguView

urlpatterns = [


    # common urls


    url(r'^admin/', admin.site.urls, name='admin'),
    url(r'^$', RedirectView.as_view(url='login/', permanent=False)),
    path('', include('django.contrib.auth.urls'), name='spodaily_login'),
    url(r'^register/', RegisterView.as_view(), name='register'),
    url(r'^register_success/', RegisterSuccessView.as_view(), name='register_success'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    url(r'^account/', AccountView.as_view(), name='account'),
    url(r'^contact/', AddContactView.as_view(), name='contact'),
    url(r'^rule_of_use/', RulesOfUseView.as_view(), name='rules_of_use'),
    url(r'^cgu/', CguView.as_view(), name='cgu'),


    # fit urls


    url(r'^fit/home/', Home.as_view(), name='home'),
    url(r'^fit/routine/', RoutineView.as_view(), name='routine'),
    url(r'^fit/program/', views.ProgramView.as_view(), name='program'),
    url(r'^fit/past_session/', PastSessionView.as_view(), name='past_session'),
    url(r'^fit/add_session/', views.AddFutureSessionView.as_view(), name='add_session'),
    url(r'^fit/add_past_session/', views.AddPastSessionView.as_view(), name='add_past_session'),
    url(r'^fit/add_program_session/', views.AddProgramSessionView.as_view(), name='add_program_session'),
    path('fit/delete_past_session/<uuid:pk>/', DeletePastSessionView.as_view(), name='delete_past_session'),
    path('fit/delete_future_session/<uuid:pk>/', DeleteFutureSessionView.as_view(), name='delete_future_session'),
    path('fit/delete_program_session/<uuid:pk>/', DeleteProgramSessionView.as_view(), name='delete_program_session'),
    path('fit/delete_activity/<uuid:pk>/', DeleteActivityView.as_view(), name='delete_activity'),
    path('fit/delete_future_activity/<uuid:pk>/', DeleteFutureActivityView.as_view(), name='delete_future_activity'),
    path('fit/delete_program_activity/<uuid:pk>/', DeleteProgramActivityView.as_view(), name='delete_program_activity'),
    path('fit/update_activity/<uuid:pk>/', UpdateActivityView.as_view(), name='update_activity'),
    path('fit/update_future_activity/<uuid:pk>/', UpdateFutureActivityView.as_view(), name='update_future_activity'),
    path('fit/update_program_activity/<uuid:pk>/', UpdateProgramActivityView.as_view(), name='update_program_activity'),
    path('fit/add_future_activity/<uuid:fk>/', AddFutureActivityView.as_view(), name='add_future_activity'),
    path('fit/add_program_activity/<uuid:fk>/', AddProgramActivityView.as_view(), name='add_program_activity'),
    path('fit/session_done/<uuid:fk>/', MarkSessionAsDone.as_view(), name='session_done'),
    path('fit/duplicate_program_session/<uuid:fk>/', DuplicateProgramSessionView.as_view(), name='duplicate_program_session'),
    path('fit/add_past_activity/<uuid:fk>/', AddPastActivityView.as_view(), name='add_past_activity'),
    url(r'^fit/exercise_guide/', ExerciseGuideView.as_view(), name='exercise_guide'),
    path('fit/muscle/<uuid:fk>/', MuscleView.as_view(), name='muscle'),


    # food urls


    url(r'^food/home/', FoodHome.as_view(), name='food_home'),
]
