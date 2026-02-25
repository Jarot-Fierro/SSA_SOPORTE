from django.utils.deprecation import MiddlewareMixin

from users.models import UserRole


class UserRolesMiddleware(MiddlewareMixin):

    def process_request(self, request):
        user = getattr(request, 'user', None)

        # valores por defecto para evitar errores si no hay sesión
        request.user_roles = {}
        request.establecimiento = None

        if user and user.is_authenticated:
            # Establecimiento desde el usuario
            request.establecimiento = user.establecimiento

            # Traer roles asignados al usuario
            roles = UserRole.objects.filter(user_id=user).select_related('role_id')

            permisos = {
                "mantenedores": 0,
                "organizacion": 0,
                "plan": 0,
                "chip": 0,
                "celular": 0,
                "computador": 0,
                "toner": 0,
                "impresora": 0,
                "usuarios": 0,
                "establecimiento": 0,

            }

            # combinar permisos (si tuviera más de un rol, se usa el mayor)
            for user_role in roles:
                role = user_role.role_id
                for perm in permisos.keys():
                    permisos[perm] = max(permisos[perm], getattr(role, perm))

            request.user_roles = permisos

        return None
