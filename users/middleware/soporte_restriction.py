from django.shortcuts import redirect


class RestrictSoporteMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # Obtener el nombre de la URL actual
            from django.urls import resolve
            try:
                current_url_name = resolve(request.path_info).url_name
            except:
                current_url_name = None

            # URLs destinadas exclusivamente a SOPORTE
            soporte_url_names = [
                'ticket_list',
                'ticket_create',
                'ticket_update',
            ]

            if getattr(request.user, 'usuario_soporte', False):
                # URLs permitidas para el usuario de soporte (lista blanca)
                allowed_for_soporte = [
                    'ticket_list',
                    'ticket_create',
                    'ticket_update',
                    'ticket_asignar_equipo',
                    'get_equipos_ajax',
                    'ticket_eliminar_equipo',
                    'login',
                    'logout',
                    'dashboard',
                    'dashboard_data',
                    'home',
                ]

                # Si intenta acceder al admin o a una URL no permitida
                if request.path.startswith('/admin/') or (
                        current_url_name and current_url_name not in allowed_for_soporte):
                    if current_url_name != 'ticket_list':
                        return redirect('ticket_list')
            else:
                # El usuario NO es de soporte. No puede acceder a secciones de soporte.
                if current_url_name in soporte_url_names:
                    return redirect('dashboard')

        response = self.get_response(request)
        return response
