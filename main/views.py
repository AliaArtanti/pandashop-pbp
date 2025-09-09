from django.shortcuts import render

def show_main(request):
    context = {
        'app_name' : 'pandashop',
        'name': 'Alia Artanti 2406439425',
        'class': 'PBP F'
    }

    return render(request, "main.html", context)