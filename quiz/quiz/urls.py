"""quiz URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("quiz/<int:pk>", detail_view, name="detail",),
    path("quiz/<int:pk>/u", QuizUpdateView.as_view(), name="update"),

    path("", list_view, name="list"),
    path("quiz/create", CreateView.as_view(), name="create"),
    path("quiz/q", search_view, name="search"),
    path("question/create", CreateViewQuest.as_view(), name="create-q"),

    path("question/<int:pk>", question_view, name="question"),
    path("question/<int:pk>/u", QuestionUpdateView.as_view(), name="question-u"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
