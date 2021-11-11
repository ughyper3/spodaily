import datetime

from django.contrib import messages
from django.contrib.auth.backends import UserModel
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.generic import TemplateView, DeleteView, CreateView, UpdateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from spodaily_api.models import Activity, Session, User
from spodaily_api.models_queries import get_activities_by_session, \
    get_muscles, get_muscle_by_uuid, get_exercise_by_muscle, get_past_sessions_by_user, get_session_number_by_user, \
    get_tonnage_number_by_user, get_calories_burn_by_user, get_future_sessions_by_user, get_session_program_by_user

from spodaily_api.forms import LoginForm, CreateUserForm, EditUserForm, AddSessionForm, AddActivityForm, AddContactForm, \
    AddSessionProgramForm, AddSessionDuplicateForm, SessionDoneForm
from spodaily_api.models_queries import get_graph_of_exercise


class LoginView(TemplateView):
    template_name = "registration/login.html"

    def post(self, request):
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            user = authenticate(email=login_form.cleaned_data.get('email'),
                                password=login_form.cleaned_data.get('password'))
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('home'))

            else:
                messages.error(request, 'username or password not correct')

        return HttpResponseRedirect(reverse('login'))


class Home(LoginRequiredMixin, TemplateView):
    template_name = "spodaily_api/home.html"

    def get(self, request, *args, **kwargs):
        context = {}
        user = request.user
        today = datetime.date.today()
        number_of_session = get_session_number_by_user(user.uuid)
        number_of_tonnage = get_tonnage_number_by_user(user.uuid)
        number_of_calories = get_calories_burn_by_user(user.uuid)
        sdt_data = get_graph_of_exercise(request, 'Soulevé de terre')
        squat_data = get_graph_of_exercise(request, 'Squat')
        bench_data = get_graph_of_exercise(request, 'Développé couché')
        number_of_session = 1
        session = get_future_sessions_by_user(user.uuid, number_of_session).values('name', 'uuid', 'date')
        activities_list = []
        for ses in session:
            activity = get_activities_by_session(ses['uuid'])
            activities_list.append(activity)
            ses['color'] = 'white' if ses['date'] >= today else '#BA4545'
        context['session'] = session
        context['activity'] = activities_list
        context['sdt_labels'] = sdt_data[0]
        context['sdt_data'] = sdt_data[1]
        context['sdt_exercise'] = sdt_data[2]
        context['squat_labels'] = squat_data[0]
        context['squat_data'] = squat_data[1]
        context['squat_exercise'] = squat_data[2]
        context['bench_labels'] = bench_data[0]
        context['bench_data'] = bench_data[1]
        context['bench_exercise'] = bench_data[2]
        context['number_of_session'] = number_of_session
        context['number_of_tonnage'] = number_of_tonnage['sum']
        context['number_of_calories'] = number_of_calories

        return render(request, self.template_name, context)


class AddFutureSessionView(LoginRequiredMixin, TemplateView):
    template_name = "spodaily_api/add_session.html"

    def get(self, request, *args, **kwargs):
        form = AddSessionForm()
        context = {'form': form}
        return render(request, 'spodaily_api/add_session.html', context)

    def post(self, request, *args, **kwargs):
        form = AddSessionForm(request.POST)
        form.instance.user = request.user
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('routine'))


class AddFutureActivityView(LoginRequiredMixin, CreateView):
    template_name = "spodaily_api/add_activity.html"
    model = Activity
    success_url = '/'

    def get(self, request, *args, **kwargs):
        form = AddActivityForm()
        session = Session.objects.get(uuid=kwargs['fk'])
        context = {'form': form,
                   'session': session}
        return render(request, 'spodaily_api/add_activity.html', context)

    def post(self, request, *args, **kwargs):
        form = AddActivityForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.instance.session_id = Session.objects.get(uuid=kwargs['fk'])
            form.save()
            return HttpResponseRedirect(reverse('routine'))


class AddProgramActivityView(LoginRequiredMixin, CreateView):
    template_name = "spodaily_api/add_activity.html"
    model = Activity
    success_url = '/'

    def get(self, request, *args, **kwargs):
        form = AddActivityForm()
        session = Session.objects.get(uuid=kwargs['fk'])
        context = {'form': form,
                   'session': session}
        return render(request, 'spodaily_api/add_activity.html', context)

    def post(self, request, *args, **kwargs):
        form = AddActivityForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.instance.session_id = Session.objects.get(uuid=kwargs['fk'])
            form.save()
            return HttpResponseRedirect(reverse('program'))


class AddPastSessionView(LoginRequiredMixin, TemplateView):
    template_name = "spodaily_api/add_session.html"

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
    template_name = "spodaily_api/add_activity.html"
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
    template_name = "spodaily_api/add_activity.html"
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
            return HttpResponseRedirect(reverse('routine'))


class DeletePastSessionView(LoginRequiredMixin, DeleteView):
    template_name = "spodaily_api/delete_session.html"
    model = Session
    success_url = reverse_lazy('past_session')


class DeleteFutureSessionView(LoginRequiredMixin, DeleteView):
    template_name = "spodaily_api/delete_session.html"
    model = Session
    success_url = reverse_lazy('routine')


class DeleteProgramSessionView(LoginRequiredMixin, DeleteView):
    template_name = "spodaily_api/delete_session.html"
    model = Session
    success_url = reverse_lazy('program')


class DeleteActivityView(LoginRequiredMixin, DeleteView):
    template_name = "spodaily_api/delete_activity.html"
    model = Activity
    success_url = reverse_lazy('past_session')

    def get(self, request, *args, **kwargs):
        activity_uuid = request.get_full_path()[26:-1]
        session = Session.objects.filter(activity_session_id=activity_uuid).values('name', 'date')[0]
        activity = Activity.objects.filter(uuid=activity_uuid).values('exercise_id__name')[0]
        context = {'session': session, 'activity': activity}
        return render(request, self.template_name, context)


class DeleteFutureActivityView(LoginRequiredMixin, DeleteView):
    template_name = "spodaily_api/delete_activity.html"
    model = Activity
    success_url = reverse_lazy('routine')

    def get(self, request, *args, **kwargs):
        activity_uuid = request.get_full_path()[33:-1]
        session = Session.objects.filter(activity_session_id=activity_uuid).values('name', 'date')[0]
        activity = Activity.objects.filter(uuid=activity_uuid).values('exercise_id__name')[0]
        context = {'session': session, 'activity': activity}
        return render(request, self.template_name, context)


class DeleteProgramActivityView(LoginRequiredMixin, DeleteView):
    template_name = "spodaily_api/delete_activity.html"
    model = Activity
    success_url = reverse_lazy('program')

    def get(self, request, *args, **kwargs):
        activity_uuid = request.get_full_path()[34:-1]
        session = Session.objects.filter(activity_session_id=activity_uuid).values('name', 'date')[0]
        activity = Activity.objects.filter(uuid=activity_uuid).values('exercise_id__name')[0]
        context = {'session': session, 'activity': activity}
        return render(request, self.template_name, context)


class ExerciseGuideView(LoginRequiredMixin, TemplateView):
    template_name = 'spodaily_api/exercise_guide.html'

    def get(self, request, *args, **kwargs):
        muscles = get_muscles()
        context = {'muscle': muscles}
        return render(request, self.template_name, context)


class MuscleView(LoginRequiredMixin, TemplateView):
    template_name = 'spodaily_api/muscle.html'

    def get(self, request, *args, **kwargs):
        uuid = request.get_full_path()[17:-1]  # disgusting way to get url
        muscle = get_muscle_by_uuid(uuid)
        exercise = get_exercise_by_muscle(uuid)
        context = {'muscle': muscle,
                   'exercise': exercise}
        return render(request, self.template_name, context)


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
            return HttpResponseRedirect(reverse('home'))


class LogoutView(LoginRequiredMixin, TemplateView):
    template_name = 'registration/logged_out.html'

    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse('dlc_login'))


class RoutineView(LoginRequiredMixin, TemplateView):
    template_name = 'spodaily_api/routine.html'

    def get(self, request, *args, **kwargs):
        context = {}
        today = datetime.date.today()
        user = request.user
        number_of_session = 8
        session = get_future_sessions_by_user(user.uuid, number_of_session).values()
        activities_list = []
        for ses in session:
            activity = get_activities_by_session(ses['uuid'])
            activities_list.append(activity)
            ses['color'] = 'white' if ses['date'] >= today else '#BA4545'
        context['session'] = session
        context['activity'] = activities_list
        return render(request, self.template_name, context)


class ContactView(LoginRequiredMixin, TemplateView):
    template_name = 'spodaily_api/contact.html'

    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, self.template_name, context)


class RulesOfUseView(LoginRequiredMixin, TemplateView):
    template_name = 'spodaily_api/rules_of_use.html'

    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, self.template_name, context)


class PastSessionView(LoginRequiredMixin, TemplateView):
    template_name = "spodaily_api/past_session.html"

    def get(self, request, *args, **kwargs):
        context = {}
        user = request.user
        session = get_past_sessions_by_user(user.uuid).values()
        activities_list = []
        for ses in session:
            activity = get_activities_by_session(ses['uuid'])
            activities_list.append(activity)

        context['session'] = session
        context['activity'] = activities_list
        return render(request, 'spodaily_api/past_session.html', context)


class RegisterView(TemplateView):
    template_name = "registration/register.html"

    def get(self, request, *args, **kwargs):
        form = CreateUserForm()
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = CreateUserForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            email = form.cleaned_data['email']
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('emails/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
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
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


class RegisterSuccessView(TemplateView):
    template_name = 'registration/register_success.html'

    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, self.template_name, context)


class UpdateActivityView(UpdateView):
    model = Activity
    fields = ['exercise_id', 'weight', 'rest', 'repetition', 'sets']
    template_name = 'spodaily_api/update_activity.html'
    success_url = reverse_lazy('past_session')


class UpdateFutureActivityView(UpdateView):
    model = Activity
    fields = ['exercise_id', 'weight', 'rest', 'repetition', 'sets']
    template_name = 'spodaily_api/update_activity.html'
    success_url = reverse_lazy('routine')


class UpdateProgramActivityView(UpdateView):
    model = Activity
    fields = ['exercise_id', 'weight', 'rest', 'repetition', 'sets']
    template_name = 'spodaily_api/update_activity.html'
    success_url = reverse_lazy('program')


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


class ProgramView(LoginRequiredMixin, TemplateView):
    template_name = 'spodaily_api/program.html'

    def get(self, request, *args, **kwargs):
        context = {}
        session = get_session_program_by_user(request.user.uuid).values()
        activities_list = []
        for ses in session:
            activity = get_activities_by_session(ses['uuid'])
            activities_list.append(activity)

        context['session'] = session
        context['activity'] = activities_list

        return render(request, self.template_name, context)


class AddProgramSessionView(LoginRequiredMixin, TemplateView):
    template_name = 'spodaily_api/add_program_session.html'

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
    template_name = "spodaily_api/duplicate_program_session.html"

    def get(self, request, *args, **kwargs):
        session_uuid = request.get_full_path()[36:-1]
        session = Session.objects.get(uuid=session_uuid)
        form = AddSessionDuplicateForm()
        context = {'session': session,
                   'form': form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = AddSessionDuplicateForm(request.POST)
        form.instance.user = request.user
        if form.is_valid():
            session_uuid = request.get_full_path()[36:-1]
            session = Session.objects.get(uuid=session_uuid)
            activities = Activity.objects.filter(session_id=session_uuid)
            session_2 = session
            session_2.pk = None
            session_2.is_program = False
            session_2.date = form.instance.date
            session_2.save()
            for activity in activities:
                activity_2 = activity
                activity_2.pk = None
                activity_2.session_id = session
                activity_2.save()
            return HttpResponseRedirect(reverse('routine'))
        else:
            return HttpResponseRedirect(reverse('home'))


class MarkSessionAsDone(LoginRequiredMixin, TemplateView):
    template_name = "spodaily_api/session_done.html"

    def get(self, request, *args, **kwargs):
        session_uuid = request.get_full_path()[23:-1]
        session = Session.objects.get(uuid=session_uuid)
        form = SessionDoneForm()
        context = {'form': form,
                   'session': session
                   }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = SessionDoneForm(request.POST)
        form.instance.user = request.user
        if form.is_valid():
            session_uuid = request.get_full_path()[23:-1]
            session = Session.objects.get(uuid=session_uuid)
            session.is_done = True
            session.save()
            return HttpResponseRedirect(reverse('past_session'))
        else:
            return HttpResponseRedirect(reverse('home'))