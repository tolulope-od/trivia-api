import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_resource(request_arg: object, resources: list):
    page: int = request_arg.args.get('page', 1, type=int)
    start: int = (page - 1) * QUESTIONS_PER_PAGE
    end: int = start + QUESTIONS_PER_PAGE

    resources: list = [resource.format() for resource in resources]
    resources_paginated = resources[start:end]

    return resources_paginated


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
    Set up CORS. Allow '*' for origins.
    '''
    CORS(app, resources={r'/*': {'origins': '*'}})

    '''
    Use the after_request decorator to set Access-Control-Allow
    '''

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response


    @app.route('/categories')
    def get_categories():
        """
        get all available categories
        :return:
          JSON -- A JSON object with the status of the request and all categories
        """
        categories: list = Category.query.all()
        formatted_categories = [category.format() for category in categories]
        return jsonify({
            'success': True,
            'categories': formatted_categories
        })

    @app.route('/questions')
    def get_paginated_questions():
        """
        request questions from the database paginated to 10 items per page
        :return:
          JSON -- A JSON object with the questions and total number of questions in the db
        """
        questions: list = Question.query.order_by(Question.id).all()
        formatted_questions: list = paginate_resource(request, questions)

        if len(formatted_questions) == 0:
            abort(404)

        categories: list = Category.query.order_by(Category.id).all()
        formatted_categories = [category.format() for category in categories]

        return jsonify({
            'success': True,
            'questions': formatted_questions,
            'total_questions': len(questions),
            'categories': formatted_categories
        }), 200

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        """
        delete a question using the question ID
        :param question_id: integer -- ID of the question to be deleted
        :return:
          JSON -- A JSON object that contains the success status of the request, the deleted question id and the total
          number of questions
        """
        try:
            question: object = Question.query.filter(Question.id == question_id).one_or_none()

            if question is None:
                abort(404)

            question.delete()

            return jsonify({
                'success': True,
                'deleted': question_id,
                'total_questions': len(Question.query.all())
            }), 200
        except:
            abort(422)

    @app.route('/questions', methods=['POST'])
    def create_question():
        """
        Create a new question with the question, answer, category and difficulty score
        :return:
          JSON -- A JSON object with the status of the request and the ID of the new question
        """
        body: object = request.get_json()

        question: str = body.get('question', None)
        answer: str = body.get('answer', None)
        category: str = body.get('category', None)
        difficulty: str = body.get('difficulty', None)

        try:
            if question is None or answer is None or category is None or difficulty is None:
                abort(400)

            question: object = Question(question=question, answer=answer, category=category, difficulty=difficulty)
            question.insert()

            questions: list = Question.query.order_by(Question.id).all()
            current_questions: list = paginate_resource(request, questions)

            return jsonify({
                'success': True,
                'created': question.id,
                'questions': current_questions,
                'total_questions': len(Question.query.all())
            }), 201

        except:
            abort(422)

    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        """
        Get questions based on a search term
        :return:
          JSON -- A JSON object with a list of questions matching the search term
        """
        body: object = request.get_json()

        search_term: str = body.get('searchTerm', None)

        try:
            if search_term is None:
                abort(400)

            questions: list = Question.query.filter(Question.question.ilike('%{}%'.format(search_term))).all()
            formatted_questions: list = [question.format() for question in questions]

            return jsonify({
                'success': True,
                'questions': formatted_questions,
                'total_questions': len(questions)
            }), 200
        except:
            abort(422)

    @app.route('/categories/<int:category_id>/questions')
    def get_questions_by_category(category_id):
        """
        Get questions based on category
        :param category_id: integer -- The ID of the category
        :return:
          JSON - A JSON object with questions that match the given category
        """
        questions: list = Question.query.filter(Question.category == category_id).all()
        current_category: object = Category.query.filter(Category.id == category_id).one_or_none()

        if current_category is None:
            abort(404)

        formatted_questions: list = [question.format() for question in questions]

        return jsonify({
            'success': True,
            'questions': formatted_questions,
            'total_questions': len(questions),
            'current_category': current_category.format()
        }), 200

    @app.route('/quizzes', methods=['POST'])
    def get_quiz():
        """
        get a random quiz question selected from a particular category or from all categories
        :return:
          JSON -- A JSON object with a random question and the total number of questions that exist
        """
        body: dict = request.get_json()

        previous_questions: list = body.get('previous_questions', None)
        quiz_category: dict = body.get('quiz_category', None)

        try:
            if quiz_category['id'] != 0:
                formatted_questions: list = [question.format() for question in Question.query.filter(
                    Question.category == quiz_category['id'], Question.id.notin_(previous_questions)).all()]

            else:
                formatted_questions: list = [question.format() for question in Question.query.all()]

            if len(formatted_questions) == 0:
                return jsonify({
                    'success': True,
                    'question': None
                }), 200

            questions_count: int = len(formatted_questions)
            random_index: int = random.randint(0, questions_count - 1)
            random_question: dict = formatted_questions[random_index]

            return jsonify({
                'success': True,
                'question': random_question,
                }), 200

        except:
            abort(422)



    '''
    @TODO: 
    Create error handlers for all expected errors 
    including 404 and 422. 
    '''
    @app.errorhandler(404)
    def not_found_err(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'resource not found'
        }), 404

    @app.errorhandler(400)
    def bad_request_err(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'bad request, please format and try again'
        }), 400

    @app.errorhandler(405)
    def method_not_allowed_err(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'method not allowed'
        }), 405

    @app.errorhandler(422)
    def unprocessable_error(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable request'
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'an error occurred on the server please try again'
        }), 500

    return app
