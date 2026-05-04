from django.shortcuts import redirect


class RestrictSoporteMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and getattr(request.user, 'usuario_soporte', False):
            # URLs permitidas para el usuario de soporte
            allowed_url_names = [
                'usuarios_dpto_list',
                'usuarios_dpto_create',
                'usuarios_dpto_update',
                'usuarios_dpto_detail',
                'logout',
                'login',
            ]

            # Obtener el nombre de la URL actual
            from django.urls import resolve
            try:
                current_url_name = resolve(request.path_info).url_name
            except:
                current_url_name = None

            # Si intenta acceder al admin o a una URL no permitida
            if request.path.startswith('/admin/') or (current_url_name and current_url_name not in allowed_url_names):
                if current_url_name != 'usuarios_dpto_list':
                    return redirect('usuarios_dpto_list')

        response = self.get_response(request)
        return response
