from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import *
from datetime import datetime


# Create your views here.


@api_view(['GET'])
def index(request):
    return JsonResponse({'status': True})


@api_view(['POST'])
def create_quiz(request):
    try:
        data = request.data
        if data.get('name') is None:
            return Response({'status': False, 'message': 'Quiz name is not provided'})
        quiz = Quiz()
        quiz.name = data.get('name')
        quiz.description = data.get('description')
        quiz.label = data.get('label')
        quiz.created_at = datetime.now()
        quiz.updated_at = datetime.now()
        quiz.is_active = True
        quiz.is_deleted = False
        quiz.save()

        response_data = {'id': quiz.id, 'name': quiz.name, 'description': quiz.description, 'label': quiz.label,
                         'created_at': quiz.created_at, 'updated_at': quiz.updated_at}

        return Response({'status': True, 'data': response_data})
    except Exception as e:
        return Response({'status':False,'message':str(e)})


@api_view(['POST'])
def create_question(request):
    try:
        data = request.data
        quiz_id = data.get('quiz_id')
        if quiz_id is None:
            return Response({'status':False,'message':'Quiz id not present'})

        quiz = list(Quiz.objects.filter(id = quiz_id))

        if len(quiz) == 0:
            return  Response({'status':False,'message':'No matching quiz found'})

        chosen_quiz = quiz[0]
        question = Question()
        question.name = data.get('name')
        question.question = data.get('question')
        question.choices = data.get('choices')
        question.points = data.get('points')
        question.created_at = datetime.now()
        question.updated_at = datetime.now()
        question.is_active = True
        question.is_deleted = False
        question.save()

        question.quiz.add(chosen_quiz)
        question.save()

        return Response({'status':True,'message':'Question successfully added'})
    except Exception as e:
        return Response({'status':False,'message':str(e)})


@api_view(['POST'])
def create_answer(request):
    try:
        data = request.data
        question_id = data.get('question_id')
        if question_id is None:
            return Response({'status':False,'error':'Question id not present'})

        question = list(Question.objects.filter(id=question_id))
        if len(question) == 0:
            return  Response({'status':False,'message':'No matching Question found'})

        chosen_question = question[0]
        answer = Answer()
        answer.question = chosen_question
        answer.answer = data.get('answer')
        answer.created_at = datetime.now()
        answer.updated_at = datetime.now()
        answer.is_deleted = False
        answer.save()

        return Response({'status':True,'message':'Answer saved successfully'})
    except Exception as e:
        return Response({'status':False,'message':str(e)})


@api_view(['GET'])
def list_quizzes(request):
    try:
        quizes = Quiz.objects.all()
        response_data = []
        for i,quiz in enumerate(quizes):
            if quiz.is_deleted is False:
                quiz_detail = {'id': quiz.id, 'name': quiz.name, 'description': quiz.description, 'label': quiz.label,
                               'created_at': quiz.created_at, 'updated_at': quiz.updated_at,
                               'is_active': quiz.is_active, 'pagination_number': i}

                response_data.append(quiz_detail)
        return Response({'status':True,'data':response_data,'message':'success'})
    except Exception as e:
        return Response({'status':False,'message':str(e)})


@api_view(['POST'])
def submit_response(request):
    try:
        data = request.data
        quiz_id = data.get('quiz_id')
        user_answers = data['answers']

        quizes = list(Quiz.objects.filter(id = quiz_id))
        if len(quizes) == 0:
            return Response({'status': False, 'message': 'No matching Question found'})

        chosen_quiz = quizes[0]

        total_points = 0
        for answer in user_answers:
            question_id = answer['question_id']
            result = answer['result']
            try:
                question = Question.objects.get(id=question_id)
            except Exception as e:
                return  Response({'status':False,'message':'Invalid question id passed'})

            all_answers = Answer.objects.filter(question=question)
            for correct_answer in all_answers:
                if result == correct_answer.answer:
                    total_points += question.points

        submission = Submission()
        submission.quiz = chosen_quiz.id
        submission.username = data.get('username')
        submission.points_scored = total_points
        submission.submitted_data = data
        submission.created_at = datetime.now()
        submission.updated_at = datetime.now()
        submission.is_deleted = False
        submission.save()
        return  Response({'status':True,'data':{'points_scores':submission.points_scored},'message':'successfully submitted'})
    except Exception as e:
        return Response({'status':False,'message':str(e)})