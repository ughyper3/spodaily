import datetime
from django.contrib import messages, auth
from django.contrib.auth.backends import UserModel
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.utils.http import urlsafe_base64_decode
from django.views.generic import TemplateView, DeleteView, CreateView, UpdateView
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from spodaily_api.algorithm.fitness import Fitness
from spodaily_api.algorithm.registration import Registration
from spodaily_api.models import Activity, Session, User, FitnessGoal
from spodaily_api.forms import CreateUserForm, EditUserForm, AddSessionForm, AddActivityForm, AddContactForm, \
    AddSessionProgramForm, AddSessionDuplicateForm, SessionDoneForm, SettingsProgramSessionForm, FitnessGoalForm

"""

------- COMMON VIEWS --------

"""

class AccountView(LoginRequiredMixin, TemplateView):
    template_name = "spodaily_api/account.html"

    def get(self, request, *args, **kwargs):
        form = EditUserForm()
        context = {'edit_user_form': form}
        return render(request, 'spodaily_api/account.html', context)

    def post(self, request, *args, **kwargs):
        form = EditUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('account'))
        else:
            return HttpResponseRedirect(reverse('account'))


class LogoutView(LoginRequiredMixin, TemplateView):
    template_name = 'registration/logged_out.html'

    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse('dlc_login'))


class RulesOfUseView(LoginRequiredMixin, TemplateView):
    template_name = 'spodaily_api/rules_of_use.html'

    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, self.template_name, context)


class AddContactView(LoginRequiredMixin, TemplateView):
    template_name = "spodaily_api/contact.html"

    def get(self, request, *args, **kwargs):
        form = AddContactForm()
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = AddContactForm(request.POST)
        form.instance.user = request.user
        user_id = request.user.uuid
        if form.is_valid():
            form.save(commit=False)
            form.instance.user = User.objects.get(uuid=user_id)
            form.save()
            return HttpResponseRedirect(reverse('home'))


class RegisterView(TemplateView):
    template_name = "registration/register.html"

    def get(self, request, *args, **kwargs):
        form = CreateUserForm()
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = CreateUserForm(request.POST)
        registration = Registration()
        context = {'form': form}
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            registration.send_registration_email(user, request, form)
            messages.success(request, 'Successfully registered')
            return HttpResponseRedirect(reverse('register_success'))
        else:
            messages.error(request, 'Registration failed')
        return render(request, template_name="registration/register.html", context=context)


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, template_name="registration/confirmation_email_success.html", context={})
    else:
        return HttpResponse('Activation link is invalid!')


class RegisterSuccessView(TemplateView):
    template_name = 'registration/register_success.html'

    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, self.template_name, context)


class CguView(TemplateView):
    template_name = 'registration/cgu.html'

    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, self.template_name, context)


class DeleteAccount(LoginRequiredMixin, UpdateView):
    template_name = "spodaily_api/delete_account.html"
    model = User
    fields = ['is_active']
    success_url = reverse_lazy('register')

"""

------- FIT VIEWS --------

"""


class Home(LoginRequiredMixin, TemplateView):
    template_name = "spodaily_api/fit/home.html"

    def get(self, request, *args, **kwargs):
        fitness = Fitness()
        context = {}
        user = request.user
        today = datetime.date.today()
        number_of_sess = fitness.get_session_number_by_user(user.uuid)
        number_of_tonnage = fitness.get_tonnage_number_by_user(user.uuid)
        number_of_calories = fitness.get_calories_burn_by_user(user.uuid)
        exercise = 'Soulevé de terre'
        exercise_data = fitness.get_graph_of_exercise(request, exercise)
        number_of_session = 1
        session = fitness.get_future_sessions_by_user(user.uuid, number_of_session).values('name', 'uuid', 'date')
        activities_list = []
        for ses in session:
            activity = fitness.get_activities_by_session(ses['uuid'])
            activities_list.append(activity)
            ses['color'] = 'white' if ses['date'] >= today else '#BA4545'
        assiduity = fitness.get_frequencies_by_week(user.uuid)
        context['assiduity_labels'] = assiduity[0]
        context['assiduity_values'] = assiduity[1]
        context['session'] = session
        context['activity'] = activities_list
        context['labels'] = exercise_data[0]
        context['data'] = exercise_data[1]
        context['exercise'] = exercise_data[2]
        context['number_of_session'] = number_of_sess
        context['number_of_tonnage'] = number_of_tonnage['sum']
        context['number_of_calories'] = number_of_calories
        return render(request, self.template_name, context)


class AddFutureSessionView(LoginRequiredMixin, TemplateView):
    template_name = "spodaily_api/fit/add_session.html"

    def get(self, request, *args, **kwargs):
        form = AddSessionForm()
        context = {'form': form,
                   'today': datetime.date.today()}
        return render(request, 'spodaily_api/fit/add_session.html', context)

    def post(self, request, *args, **kwargs):
        form = AddSessionForm(request.POST)
        form.instance.user = request.user
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('home'))


class AddFutureActivityView(LoginRequiredMixin, CreateView):
    template_name = "spodaily_api/fit/add_activity.html"
    model = Activity
    success_url = '/'

    def get(self, request, *args, **kwargs):
        form = AddActivityForm()
        session = Session.objects.get(uuid=kwargs['fk'])
        context = {'form': form,
                   'session': session}
        return render(request, 'spodaily_api/fit/add_activity.html', context)

    def post(self, request, *args, **kwargs):
        form = AddActivityForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.instance.session_id = Session.objects.get(uuid=kwargs['fk'])
            form.save()
            return HttpResponseRedirect(reverse('home'))


class AddProgramActivityView(LoginRequiredMixin, CreateView):
    template_name = "spodaily_api/fit/add_activity.html"
    model = Activity
    success_url = '/'

    def get(self, request, *args, **kwargs):
        form = AddActivityForm()
        session = Session.objects.get(uuid=kwargs['fk'])
        context = {'form': form,
                   'session': session}
        return render(request, 'spodaily_api/fit/add_activity.html', context)

    def post(self, request, *args, **kwargs):
        form = AddActivityForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.instance.session_id = Session.objects.get(uuid=kwargs['fk'])
            form.save()
            return HttpResponseRedirect(reverse('program'))


class AddPastSessionView(LoginRequiredMixin, TemplateView):
    template_name = "spodaily_api/fit/add_session.html"

    def get(self, request, *args, **kwargs):
        form = AddSessionForm()
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = AddSessionForm(request.POST)
        form.instance.user = request.user
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('past_session'))


class AddPastActivityView(LoginRequiredMixin, CreateView):
    template_name = "spodaily_api/fit/add_activity.html"
    model = Activity
    success_url = '/'

    def get(self, request, *args, **kwargs):
        form = AddActivityForm()
        session = Session.objects.get(uuid=kwargs['fk'])
        context = {'form': form,
                   'session': session}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = AddActivityForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.instance.session_id = Session.objects.get(uuid=kwargs['fk'])
            form.save()
            return HttpResponseRedirect(reverse('past_session'))


class AddFutureActivityView(LoginRequiredMixin, CreateView):
    template_name = "spodaily_api/fit/add_activity.html"
    model = Activity
    success_url = '/'

    def get(self, request, *args, **kwargs):
        form = AddActivityForm()
        session = Session.objects.get(uuid=kwargs['fk'])
        context = {'form': form,
                   'session': session}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = AddActivityForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.instance.session_id = Session.objects.get(uuid=kwargs['fk'])
            form.save()
            return HttpResponseRedirect(reverse('home'))


class DeletePastSessionView(LoginRequiredMixin, DeleteView):
    template_name = "spodaily_api/fit/delete_session.html"
    model = Session
    success_url = reverse_lazy('past_session')


class DeleteFutureSessionView(LoginRequiredMixin, DeleteView):
    template_name = "spodaily_api/fit/delete_session.html"
    model = Session
    success_url = reverse_lazy('home')


class DeleteProgramSessionView(LoginRequiredMixin, DeleteView):
    template_name = "spodaily_api/fit/delete_session.html"
    model = Session
    success_url = reverse_lazy('program')


class DeleteActivityView(LoginRequiredMixin, DeleteView):
    template_name = "spodaily_api/fit/delete_activity.html"
    model = Activity
    success_url = reverse_lazy('past_session')

    def get(self, request, *args, **kwargs):
        activity_uuid = kwargs['pk']
        session = Session.objects.filter(activity_session_id=activity_uuid).values('name', 'date')[0]
        activity = Activity.objects.filter(uuid=activity_uuid).values('exercise_id__name')[0]
        context = {'session': session, 'activity': activity}
        return render(request, self.template_name, context)


class DeleteFutureActivityView(LoginRequiredMixin, DeleteView):
    template_name = "spodaily_api/fit/delete_activity.html"
    model = Activity
    success_url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        activity_uuid = kwargs['pk']
        session = Session.objects.filter(activity_session_id=activity_uuid).values('name', 'date')[0]
        activity = Activity.objects.filter(uuid=activity_uuid).values('exercise_id__name')[0]
        context = {'session': session, 'activity': activity}
        return render(request, self.template_name, context)


class DeleteProgramActivityView(LoginRequiredMixin, DeleteView):
    template_name = "spodaily_api/fit/delete_activity.html"
    model = Activity
    success_url = reverse_lazy('program')

    def get(self, request, *args, **kwargs):
        activity_uuid = kwargs['pk']
        session = Session.objects.filter(activity_session_id=activity_uuid).values('name', 'date')[0]
        activity = Activity.objects.filter(uuid=activity_uuid).values('exercise_id__name')[0]
        context = {'session': session, 'activity': activity}
        return render(request, self.template_name, context)


class ExerciseGuideView(LoginRequiredMixin, TemplateView):
    template_name = 'spodaily_api/fit/exercise_guide.html'

    def get(self, request, *args, **kwargs):
        fitness = Fitness()
        muscles = fitness.get_muscles()
        context = {'muscle': muscles}
        return render(request, self.template_name, context)


class MuscleView(LoginRequiredMixin, TemplateView):
    template_name = 'spodaily_api/fit/muscle.html'

    def get(self, request, *args, **kwargs):
        fitness = Fitness()
        uuid = kwargs['fk']
        muscle = fitness.get_muscle_by_uuid(uuid)
        exercise = fitness.get_exercise_by_muscle(uuid)
        context = {'muscle': muscle,
                   'exercise': exercise}
        return render(request, self.template_name, context)


class RoutineView(LoginRequiredMixin, TemplateView):
    template_name = 'spodaily_api/fit/routine.html'

    def get(self, request, *args, **kwargs):
        fitness = Fitness()
        context = {}
        today = datetime.date.today()
        user = request.user
        number_of_session = 8
        session = fitness.get_future_sessions_by_user(user.uuid, number_of_session).values()
        activities_list = []
        for ses in session:
            activity = fitness.get_activities_by_session(ses['uuid'])
            activities_list.append(activity)
            ses['color'] = 'white' if ses['date'] >= today else '#BA4545'
        context['session'] = session
        context['activity'] = activities_list
        return render(request, self.template_name, context)


class PastSessionView(LoginRequiredMixin, TemplateView):
    template_name = "spodaily_api/fit/past_session.html"

    def get(self, request, *args, **kwargs):
        fitness = Fitness()
        context = {}
        user = request.user
        session = fitness.get_past_sessions_by_user(user.uuid).values()
        activities_list = []
        for ses in session:
            activity = fitness.get_activities_by_session(ses['uuid'])
            activities_list.append(activity)

        context['session'] = session
        context['activity'] = activities_list
        return render(request, 'spodaily_api/fit/past_session.html', context)


class UpdateActivityView(LoginRequiredMixin, UpdateView):
    model = Activity
    fields = ['exercise_id', 'weight', 'rest', 'repetition', 'sets']
    template_name = 'spodaily_api/fit/update_activity.html'
    success_url = reverse_lazy('past_session')


class UpdateFutureActivityView(LoginRequiredMixin, UpdateView):
    model = Activity
    fields = ['exercise_id', 'weight', 'rest', 'repetition', 'sets']
    template_name = 'spodaily_api/fit/update_activity.html'
    success_url = reverse_lazy('home')


class UpdateProgramActivityView(LoginRequiredMixin, UpdateView):
    model = Activity
    fields = ['exercise_id', 'weight', 'rest', 'repetition', 'sets']
    template_name = 'spodaily_api/fit/update_activity.html'
    success_url = reverse_lazy('program')


class ProgramView(LoginRequiredMixin, TemplateView):
    template_name = 'spodaily_api/fit/program.html'

    def get(self, request, *args, **kwargs):
        fitness = Fitness()
        form = FitnessGoalForm()
        context = {}
        goals = fitness.get_fitness_goals_by_user(request.user.uuid)
        session = fitness.get_session_program_by_user(request.user.uuid).values()
        activities_list = []
        for ses in session:
            activity = fitness.get_activities_by_session(ses['uuid'])
            activities_list.append(activity)
        context['goals'] = goals
        context['session'] = session
        context['activity'] = activities_list
        context['form'] = form
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = FitnessGoalForm(request.POST)
        form.instance.user = request.user
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('program'))
        else:
            return HttpResponseRedirect(reverse('home'))


class AddProgramSessionView(LoginRequiredMixin, TemplateView):
    template_name = 'spodaily_api/fit/add_program_session.html'

    def get(self, request, *args, **kwargs):
        form = AddSessionProgramForm()
        context = {'form': form}

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = AddSessionProgramForm(request.POST)
        form.instance.user = request.user
        if form.is_valid():
            form.save(commit=False)
            form.instance.is_program = True
            form.save()
            return HttpResponseRedirect(reverse('program'))
        else:
            return HttpResponseRedirect(reverse('home'))


class DuplicateProgramSessionView(LoginRequiredMixin, TemplateView):
    template_name = "spodaily_api/fit/duplicate_program_session.html"

    def get(self, request, *args, **kwargs):
        session_uuid = kwargs['fk']
        session = Session.objects.get(uuid=session_uuid)
        form = AddSessionDuplicateForm()
        context = {'session': session,
                   'form': form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = AddSessionDuplicateForm(request.POST)
        form.instance.user = request.user
        fitness = Fitness()
        if form.is_valid():
            fitness.duplicate_session(kwargs['fk'], form)
            return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponseRedirect(reverse('home'))


class MarkSessionAsDone(LoginRequiredMixin, TemplateView):
    template_name = "spodaily_api/fit/session_done.html"

    def get(self, request, *args, **kwargs):
        session_uuid = kwargs['fk']
        session = Session.objects.get(uuid=session_uuid)
        form = SessionDoneForm()
        context = {'form': form,
                   'session': session
                   }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = SessionDoneForm(request.POST)
        form.instance.user = request.user
        fitness = Fitness()
        if form.is_valid():
            fitness.mark_session_as_done(kwargs['fk'])
            return HttpResponseRedirect(reverse('past_session'))
        else:
            return HttpResponseRedirect(reverse('home'))


class SettingsProgramSessionView(LoginRequiredMixin, TemplateView):
    template_name = "spodaily_api/fit/settings_programme_session.html"

    def get(self, request, *args, **kwargs):
        session_uuid = kwargs['fk']
        session = Session.objects.get(uuid=session_uuid)
        form = SettingsProgramSessionForm()
        context = {'session': session,
                   'form': form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = SettingsProgramSessionForm(request.POST)
        fitness = Fitness()
        if form.is_valid():
            fitness.update_session_settings(kwargs['fk'], form)
            return HttpResponseRedirect(reverse('program'))
        else:
            return HttpResponseRedirect(reverse('home'))


class DeleteGoalView(LoginRequiredMixin, DeleteView):
    template_name = "spodaily_api/fit/delete_goal.html"
    model = FitnessGoal
    success_url = reverse_lazy('program')

    def get(self, request, *args, **kwargs):
        goal_uuid = kwargs['pk']
        goal = FitnessGoal.objects.filter(uuid=goal_uuid).values('exercise__name')[0]
        context = {'goal': goal}
        return render(request, self.template_name, context)


class UpdateGoalView(LoginRequiredMixin, UpdateView):
    model = FitnessGoal
    fields = ['exercise', 'weight', 'date']
    template_name = 'spodaily_api/fit/update_goal.html'
    success_url = reverse_lazy('program')


"""

------- FOOD VIEWS --------

"""



class FoodHome(LoginRequiredMixin, TemplateView):
    template_name = 'spodaily_api/food/home.html'

    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, self.template_name, context)