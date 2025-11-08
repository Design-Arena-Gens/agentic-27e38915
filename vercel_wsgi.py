import os

from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'netball_project.settings')

application = WhiteNoise(get_wsgi_application())
app = application
