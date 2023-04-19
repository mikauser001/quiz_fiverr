from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.template.response import TemplateResponse
from django.views.generic import CreateView, UpdateView

from .models import Quiz, Question


def list_view(request):
    """"""
    all_qs = Quiz.objects.all()
    return render(request, "list.html", {
        "all": all_qs
    })


def detail_view(request, pk):
    """"""
    obj = get_object_or_404(
        Quiz, pk=pk
    )
    return render(
        request, "detail.html", {
            "q": obj
        }
    )


class QuizUpdateView(UpdateView):
    model = Quiz
    template_name = "quiz_update.html"
    fields = [
        "name", "description", "questions", "mod"
    ]


class QuestionUpdateView(UpdateView):
    model = Question
    template_name = "quest_update.html"
    fields = "__all__"


def search_view(request):

    if request.GET:
        return render(
            request, "search_r.html",
            {"result": Quiz.objects.filter(
                name__search=request.GET.get("q")
            )}
        )
    return redirect("list")


class CreateView(CreateView):
    model = Quiz
    template_name = "create.html"
    fields = [
        "name", "description", "questions", "mod"
    ]

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs) | {"quiz": True}


class CreateViewQuest(CreateView):
    model = Question
    template_name = "create.html"
    fields = "__all__"


def question_view(request, pk):
    """REVEAL QUESTION/ANSWER"""

    obj = get_object_or_404(
        Question, pk=pk
    )

    if request.htmx:
        return HttpResponse(obj.answer)

    return render(
        request, "question.html", {
            "object": obj, "others": Question.objects.all()
        }
    )


