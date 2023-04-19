from django.db import models

# Create your models here.
from django.urls import reverse


class Quiz(models.Model):

    name = models.CharField(max_length=200)
    questions = models.ManyToManyField('quiz.Question')
    mod = models.ForeignKey('user.CustomUser', on_delete=models.CASCADE, help_text="Who is the owner of this quiz?")
    participants = models.ManyToManyField('user.CustomUser', related_name="r_pac")
    description = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def points(self):
        return sum(
            [p["points"] for p in Question.objects.values_list("points", flat=True)]
        )

    def get_board(self):
        """Return the current quiz rankings& points"""
        return self.participants.filter(id_mod=False).values_list("username", "points", "rank")

    def finished(self):
        # todo
        return

    def get_absolute_url(self):
        return reverse("detail", kwargs={"pk": self.pk})


class Question(models.Model):
    headline = models.CharField(max_length=2000)
    char_body = models.TextField(null=True, blank=True)
    image_body = models.ImageField(null=True, blank=True)
    points = models.PositiveIntegerField()
    answer = models.TextField()

    def get_absolute_url(self):
        return reverse("question", kwargs={"pk": self.pk})

    def __str__(self):
        return self.headline + f" ({self.points} Points) "


class Answer(models.Model):
    char_body = models.TextField()
    user = models.ForeignKey("user.CustomUser", on_delete=models.CASCADE)
    question = models.ForeignKey("user.CustomUser", on_delete=models.CASCADE, related_name="r_answer")
    state = models.CharField(null=True, blank=True, max_length=200)

    def review(self):

        if self.char_body != self.question.answer:
            self.user.points -= self.question.points
            self.state = f"Leider falsch. - {self.question.points} Punkte"

        else:
            self.user.points += self.question.points
            self.state = f"Richtig. + {self.question.points} Punkte"

        self.user.save(update_fields=["points"])
        self.save(update_fields=["state"])