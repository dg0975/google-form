import random
import re
from collections import Counter

from django.db import transaction
from django.db.models import Count, Func
from django.db.models.functions import Length
from django.shortcuts import get_object_or_404
from django.contrib.postgres.aggregates import ArrayAgg

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from form_builder.models import *
from form_builder.utils import get_client_ip
from form_builder.utils import MODELS_TYPE

from faker import Faker


# Create your views here.
@api_view(['POST'])
def submit_form_response(request, form_id):

    body = request.data.copy()
    num_samples = body.get("num_samples", 1)
    form = Forms.objects.filter(id=form_id).first()
    if form:
        rps = [Responses(response_to=form, responder_ip=get_client_ip(request), responder=form.user,
                      responder_email=form.user.email) for j in range(num_samples)]
        with transaction.atomic():
            Responses.objects.bulk_create(rps, batch_size=500)
            resp = Responses.objects.filter(response_to=form).order_by('-id')[:num_samples]
            for each_resp in resp:
                fake = Faker()
                first_name = fake.first_name()
                last_name = fake.last_name()
                gender = random.choice(["Male", "Female", "Other"])
                age_bracket = random.choice(["<18 y", "≥18y <60y", "≥60y < 75y", "≥75y"])
                a_choice = random.choice(["Aardvark", "Abascus", "Bernie"])
                b_choice = random.choice(["Aardvark", "Abascus", "Bernie"])
                all_answer = [
                    {"question_id": 1, "answer": first_name, "question_type": "TXT"},
                    {"question_id": 2, "answer": last_name, "question_type": "TXT"},
                    {"question_id": 3, "answer": gender, "question_type": "DRP"},
                    {"question_id": 4, "answer": age_bracket, "question_type": "DRP"},
                    {"question_id": 5, "answer": [a_choice], "question_type": "CBX"},
                    {"question_id": 6, "answer": [b_choice], "question_type": "CBX"}
                ]
                answers = []
                for each_answer in all_answer:
                    answer_obj = Answer.objects.create(answer_to=Questions.objects.filter(id=each_answer.get("question_id")).first(), question_type=each_answer.get("question_type"))
                    answers.append(answer_obj)
                    MODELS_TYPE[each_answer.get("question_type")].objects.create(value=each_answer.get("answer"),
                                                                                         answer_key=answer_obj)
                each_resp.answers.add(*answers)
    else:
        return Response({"msg": "No form found."}, status=status.HTTP_204_NO_CONTENT)

    return Response({"msg": "Created."},status=status.HTTP_201_CREATED)


@api_view(['GET'])
def view_responses(request, form_id):
    form = Forms.objects.prefetch_related("questions").filter(id=form_id).first()
    if form:
        total_submissions = Responses.objects.filter(response_to__id=form_id).count()
        insights = []

        for question in form.questions.all():
            question_data = {
                "question": question.title,
                "question_type": question.question_type,
                "insights": {}
            }
            if question.question_type == "DRP":
                responses = DropdownType.objects.filter(
                    answer_key__answer_to__id=question.id
                ).values('value').annotate(count=Count('value')).order_by('-count')[:3]
                question_data["insights"]["top_options"] = [
                    {"option": r['value'], "count": r['count']} for r in responses
                ]
            elif question.question_type == "CBX":
                responses = ChoiceType.objects.filter(
                    answer_key__answer_to=question
                ).values('value').annotate(
                    options=ArrayAgg('value', ordering=('value',))
                ).annotate(count=Count("value")).order_by('-count')[:3]

                question_data["insights"]["top_options"] = [
                    {"option": r['value'], "count": r['count']} for r in responses
                ]
                # combinations = Counter(tuple(sorted(response['value'])) for response in responses if response['value'])
                # top_combinations = combinations.most_common(3)3

            #     question_data["insights"]["top_options"] = [
            #     {'combination': list(combination), 'count': count} for combination, count in top_combinations
            # ]
            elif question.question_type == "TXT":
                responses = TextType.objects.filter(
                    answer_key__answer_to=question
                ).values_list('value', flat=True)

                word_counter = Counter()
                for response_text in responses:
                    words = re.findall(r'\b\w{5,}\b', response_text.lower())
                    word_counter.update(words)

                top_words = word_counter.most_common(5)
                question_data["insights"]["top_words"] = [
                    {"word": word, "count": count} for word, count in top_words
                ]
            insights.append(question_data)
        response_data = {
            "form_title": form.title,
            "total_submissions": total_submissions,
            "insights": insights
        }
        return Response(response_data, status=status.HTTP_200_OK)
    else:
        return Response({"msg": "No Form Found"}, status=status.HTTP_204_NO_CONTENT)


# form = Forms.objects.prefetch_related("questions").filter(id=1).first()
# question = form.questions.filter(question_type="DRP")
#
# DropdownType.objects.filter(
#                 answer_key__answer_to__in=question
#             ).values('value')
