from django.shortcuts import render, redirect


def index(request):
    return render(request, 'index.html')


def redirect_to_app(request):
    if 'app' not in request.GET:
        error_message = "Please select at least one app (Weather or Password)."
        return render(request, 'index.html', {'error_message': error_message})

    selected_app = request.GET.get('app')

    return redirect(f"../{selected_app}-app/")
