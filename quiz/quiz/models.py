from django.db import models

# Create your models here.


class Quiz(models.Model):
    questions = models.ManyToManyField('quiz.Question')
    mod = models.ForeignKey('user.CustomUser', on_delete=models.CASCADE)
    participants = models.ManyToManyField('user.CustomUser', related_name="r_pac")
    description = models.TextField()

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


class Question(models.Model):
    headline = models.CharField(max_length=2000)
    char_body = models.TextField(null=True, blank=True)
    image_body = models.ImageField(null=True, blank=True)
    points = models.PositiveIntegerField()
    answer = models.TextField()


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