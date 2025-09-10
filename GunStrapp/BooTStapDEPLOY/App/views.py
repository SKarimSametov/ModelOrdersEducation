from django.views.generic import ListView, DetailView

class HomeView(ListView):
    template_name = "main.html"
    context_object_name = "ads"
