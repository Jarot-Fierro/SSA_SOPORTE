from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView
from django.views.generic import TemplateView
from django.views.generic import UpdateView

from core.mixin import DataTableMixin
from users.forms.usuarios import UserResetPasswordForm
from users.forms.usuarios_dpto import FormUsuarioDpto

MODULE_NAME = 'Usuarios'

User = get_user_model()


class UserDptoListView(DataTableMixin, TemplateView):
    template_name = 'usuarios_dpto/list.html'
    model = User

    datatable_columns = ['ID', 'Usuario', 'Establecimiento', 'Último inicio']

    datatable_order_fields = [
        'user_id', 'username',
        'establecimiento__nombre', 'last_login'
    ]

    datatable_search_fields = [
        'username__icontains',
        'email__icontains', 'establecimiento__nombre__icontains'
    ]

    url_update = 'usuarios_update'
    url_detail = 'usuarios_detail'

    # FILTRA SOLO USUARIOS DEL MISMO ESTABLECIMIENTO QUE EL USUARIO LOGUEADO
    def get_base_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return User.objects.all()

        if user.establecimiento:
            return User.objects.filter(
                establecimiento=user.establecimiento,
                is_active=True
            ).select_related('establecimiento')

        return User.objects.none()

    def render_row(self, obj):
        nombre = f"{obj.first_name or ''} {obj.last_name or ''}".strip()

        return {
            'ID': obj.user_id,  # << tu PK real
            'Usuario': obj.username,

            'Establecimiento': obj.establecimiento.nombre if obj.establecimiento else '—',
            'Último inicio': obj.last_login.strftime('%d-%m-%Y %H:%M') if obj.last_login else 'Nunca',
        }

    def get(self, request, *args, **kwargs):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.GET.get('datatable'):
            return self.get_datatable_response(request)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Usuarios del Establecimiento',
            'list_url': reverse_lazy('usuarios_list'),
            'create_url': reverse_lazy('usuarios_create'),
            'datatable_enabled': True,
            'datatable_order': [[0, 'desc']],
            'datatable_page_length': 50,
            'columns': self.datatable_columns,
        })
        return context


class UserDptoDetailView(DetailView):
    model = User
    template_name = 'usuarios_dpto/detail.html'

    def render_to_response(self, context, **response_kwargs):
        # Si es una solicitud AJAX, devolvemos solo el fragmento HTML
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            html = render_to_string(self.template_name, context=context, request=self.request)
            return HttpResponse(html)
        return super().render_to_response(context, **response_kwargs)


class UserDptoCreateView(CreateView):
    template_name = 'usuarios_dpto/form.html'
    model = User
    form_class = FormUsuarioDpto
    success_url = reverse_lazy('usuarios_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request

        return kwargs

    @transaction.atomic
    def form_valid(self, form):
        # Validación de establecimiento
        if not self.request.user.establecimiento:
            messages.error(self.request, "No tienes establecimiento asignado.")
            return redirect('no_establecimiento')

        # Asignar el establecimiento al usuario que se creará
        form.instance.establecimiento = self.request.user.establecimiento

        # Crear usuario
        user = form.save()

        messages.success(self.request, "Usuario registrado correctamente.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Hay errores en el formulario')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Nuevo Usuario '
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['module_name'] = MODULE_NAME
        return context


class UserDptoUpdateView(UpdateView):
    template_name = 'usuarios_dpto/form.html'
    model = User
    form_class = FormUsuarioDpto
    success_url = reverse_lazy('usuarios_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    @transaction.atomic
    def form_valid(self, form):
        # Validación de establecimiento
        if not self.request.user.establecimiento:
            messages.error(self.request, "No tienes establecimiento asignado.")
            return redirect('no_establecimiento')

        # Asegurarnos que el usuario se mantenga en el mismo establecimiento
        form.instance.establecimiento = self.request.user.establecimiento

        # Guardamos los cambios del usuario
        user = form.save()

        # Actualizamos la relación UserRole si cambió

        messages.success(self.request, "Usuario actualizado correctamente.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Hay errores en el formulario.")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Editar Usuario de {self.request.user.establecimiento.nombre}'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        context['module_name'] = MODULE_NAME
        return context


class UserDptoChangePasswordView(LoginRequiredMixin, View):
    """
    Permite al usuario logueado cambiar su propia contraseña.
    """
    login_url = 'login'
    template_name = 'usuarios_dpto/change_password.html'

    def get(self, request, *args, **kwargs):
        form = UserResetPasswordForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = UserResetPasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['password1']
            user = request.user
            user.set_password(new_password)
            user.save()
            messages.success(request, 'Tu contraseña se ha actualizado correctamente.')
            return redirect(reverse_lazy('usuarios_update', kwargs={'pk': request.user.pk}))

        return render(request, self.template_name, {'form': form})
