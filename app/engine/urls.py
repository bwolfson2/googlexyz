from django.urls import path
from engine.views import query, results, about 
import os 

urlpatterns = [
    path('',query, name="query"),
    path('about', about, name="about")
]

if os.environ.get("ENVIRONMENT") != "light":
    urlpatterns.append(path('results', results, name="results"))
