from django.shortcuts import redirect

class RedirectAllToHomeMiddleware:
    """
    This middleware will redirect all requests to the homepage ('/')
    unless the user is accessing the homepage or admin page.
    """
    def __init__(self, get_response):
        # This is the initialization step. It receives the get_response callable.
        self.get_response = get_response

    def __call__(self, request):
        # This method will be called for each request.
        
        # Check if the requested path is not the homepage ('/') or the admin page
        if request.path != '/' and not request.path.startswith('/admin'):
            return redirect('/')  # Redirect to the homepage if not the homepage or admin
        
        # If it's the homepage or admin, continue with the request
        response = self.get_response(request)
        
        return response