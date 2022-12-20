from .models import Link

def links(request):
    return {'links':Link.objects.all()}