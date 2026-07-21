import os
from django.http import FileResponse, HttpResponse
from django.conf import settings

FLUTTER_DIR = os.path.join(settings.BASE_DIR, 'flutter_web')

def serve_flutter(request, **kwargs):
    path = request.path.lstrip('/')
    # Strip leading 'app/' prefix
    if path.startswith('app/'):
        path = path[4:]

    file_path = os.path.join(FLUTTER_DIR, path)

    if os.path.isfile(file_path):
        return FileResponse(open(file_path, 'rb'))

    # Always fall back to index.html for Flutter routing
    index = os.path.join(FLUTTER_DIR, 'index.html')
    return HttpResponse(open(index, 'rb').read(), content_type='text/html')
