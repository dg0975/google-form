from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin


from form_builder.models import Forms, Questions, Choices, Answer, DropdownType, TextType, Responses, ChoiceType


@admin.register(Forms)
class FormsAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    search_fields = ('title',)
    list_display = ('id', 'created', 'modified', 'title',)


@admin.register(Questions)
class QuestionsAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    search_fields = ('title',)
    list_display = ('id', 'created', 'modified', 'label',)
    list_filter = ("constraints", "question_type")


@admin.register(Choices)
class ChoicesAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'created', 'modified', 'choice', )


@admin.register(Answer)
class AnswerAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'created', 'modified', 'answer_to', )


@admin.register(DropdownType)
class DropdownTypeAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'created', 'modified', 'value', "answer_key")


@admin.register(TextType)
class TextTypeAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'created', 'modified', 'value', "answer_key")


@admin.register(ChoiceType)
class ChoiceTypeAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'created', 'modified', 'value', "answer_key")


@admin.register(Responses)
class ResponsesAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'created', 'modified', 'response_to', "responder_ip", "responder_email")