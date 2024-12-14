from django.contrib.auth.models import User
from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField
from rtb.managers import ModelManager


from rtb.mixin import StatusMixin
from form_builder.constants import CONSTRAINTS_TYPE, QUESTION_TYPE


class Choices(StatusMixin):
    choice = models.CharField(max_length=25)
    is_answer = models.BooleanField(default=False)

    objects = ModelManager()

    class Meta:
        db_table = "Choices"
        verbose_name = "Choice"
        verbose_name_plural = "Choices"

    def __str__(self):
        if self.choice:
            return self.choice
        return str(self.id)


class Questions(StatusMixin):
    label = models.CharField(max_length=250, null=False, blank=False)
    title = models.TextField(null=False, blank=False)
    order = models.SmallIntegerField(null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    constraints = models.CharField(choices=CONSTRAINTS_TYPE, default="OP", max_length=2)
    question_type = models.CharField(choices=QUESTION_TYPE, default="TXT", max_length=3)
    choices = models.ManyToManyField(Choices, related_name="choices", null=True, blank=True)

    objects = ModelManager()

    class Meta:
        db_table = "Questions"
        verbose_name = "Question"
        verbose_name_plural = "Questions"

    def __str__(self):
        if self.label:
            return self.label


class Forms(StatusMixin):
    title = models.CharField(max_length=500, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_request', default=None)
    questions = models.ManyToManyField("Questions", blank=True)

    objects = ModelManager()

    class Meta:
        db_table = "Forms"
        verbose_name = "Form"
        verbose_name_plural = "Forms"


class Answer(StatusMixin):
    answer_to = models.ForeignKey(Questions, on_delete = models.CASCADE , related_name = "answer_to")
    question_type = models.CharField(max_length=50, null=False, blank=False)

    objects = ModelManager()

    class Meta:
        db_table = "Answer"
        verbose_name = "Answer"
        verbose_name_plural = "Answers"


class FileType(StatusMixin):
    value = models.FileField(upload_to="answer_files", null=False, blank=False)
    answer_key = models.ForeignKey(Answer, on_delete = models.CASCADE , null=False, related_name = "answer_file")

    objects = ModelManager()

    class Meta:
        db_table = "FileType"
        verbose_name = "FileType"
        verbose_name_plural = "FileTypes"


class DateType(StatusMixin):
    value = models.DateField(null=False, blank=False)
    answer_key = models.ForeignKey(Answer, on_delete = models.CASCADE, null=False,related_name = "answer_date")

    objects = ModelManager()

    class Meta:
        db_table = "DateType"
        verbose_name = "DateType"
        verbose_name_plural = "DateTypes"


class TimeType(StatusMixin):
    value = models.TimeField(null=False, blank=False)
    answer_key = models.ForeignKey(Answer, on_delete=models.CASCADE, null=False,related_name = "answer_time_type")

    objects = ModelManager()

    class Meta:
        verbose_name = "TimeType"
        verbose_name_plural = "TimeTypes"


class ChoiceType(StatusMixin):
    value = ArrayField(models.CharField(max_length=50,null=False, blank=False), null=False, blank=False)
    answer_key = models.ForeignKey(Answer, on_delete = models.CASCADE, null=False, related_name = "answer_choice")

    objects = ModelManager()

    class Meta:
        verbose_name = "ChoiceType"
        verbose_name_plural = "ChoiceType"


class DropdownType(StatusMixin):
    value = models.CharField(max_length=50,null=False, blank=False)
    answer_key = models.ForeignKey(Answer, on_delete = models.CASCADE, null=False, related_name = "answer_dropdown")

    objects = ModelManager()

    class Meta:
        db_table = "DropdownType"
        verbose_name = "DropdownType"
        verbose_name_plural = "DropdownTypes"


class MatrixType(StatusMixin):
    value = ArrayField(models.IntegerField(null=False, blank=False), null=False, blank=False)
    answer_key = models.ForeignKey(Answer, on_delete = models.CASCADE, null=False, related_name = "answer_matrix")

    objects = ModelManager()

    class Meta:
        db_table = "MatrixType"
        verbose_name = "MatrixType"
        verbose_name_plural = "MatrixType"


class TextType(StatusMixin):
    value = models.CharField(null=False, blank=False, max_length=250)
    specification = models.JSONField(
        default=dict
    )
    answer_key = models.ForeignKey(Answer, on_delete = models.CASCADE, null=False, related_name = "answer_text")

    objects = ModelManager()

    class Meta:
        db_table = "TextType"
        verbose_name = "TextType"
        verbose_name_plural = "TextTypes"


class Responses(StatusMixin):
    response_to = models.ForeignKey(Forms, on_delete = models.CASCADE, related_name = "response_to")
    responder_ip = models.CharField(max_length=30)
    responder = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "responder", blank = True, null = True)
    responder_email = models.EmailField(blank = True)
    answers = models.ManyToManyField(Answer, related_name = "response")

    objects = ModelManager()

    class Meta:
        db_table = "Response"
        verbose_name = "Response"
        verbose_name_plural = "Responses"