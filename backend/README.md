# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

## Database Setup

With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:

```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application.

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle GET requests for all available categories.
4. Create an endpoint to DELETE question using a question ID.
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score.
6. Create a POST endpoint to get questions based on category.
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422 and 500.

## API Reference

The following HTTP methods are allowed on the API: `GET`, `POST`, `DELETE`

##### Status Code Summary

| _Status code_       |                                                                   _Description_ |
| :------------------ | ------------------------------------------------------------------------------: |
| 200 - OK            |                                                   Everything worked as expected |
| 201 - Created       |                                         A new resource was successfully created |
| 400 - Bad Request   |         The request was unacceptable, often due to a missing required parameter |
| 404 - Not Found     |                                           The requested resource does not exist |
| 405 - Not Allowed   |                                   The HTTP method is not allowed on an endpoint |
| 422 - Unprocessable | The request was unprocessable, this could be due to supplying a wrong data type |
| 500 - Server Error  |                                              Something went wrong on the server |

##### Endpoints

**GET** /categories

This endpoint returns a JSON object with all available categories.

_Sample Request_

```bash
$ curl -X GET localhost:5000/categories
```

_Sample Response_

```JSON
{
  "categories": [
    {
      "id": 1,
      "type": "Science"
    },
    {
      "id": 2,
      "type": "Art"
    },
    {
      "id": 3,
      "type": "Geography"
    },
    {
      "id": 4,
      "type": "History"
    },
    {
      "id": 5,
      "type": "Entertainment"
    },
    {
      "id": 6,
      "type": "Sports"
    }
  ],
  "success": true
}
```

**GET** /questions
This endpoint returns a list of questions paginated to 10 questions per page. It also takes in a `page` query parameter in the request that specifies the page to be returned from the server.

_Sample Request_

```bash
$ curl -X GET localhost:5000/questions?page=2
```

_Sample Response_

```JSON
{
  "categories": [
    {
      "id": 1,
      "type": "Science"
    },
    {
      "id": 2,
      "type": "Art"
    }
  ],
  "questions": [
    {
      "answer": "Escher",
      "category": 2,
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist–initials M C was a creator of optical illusions?"
    },
    ...
    {
      "answer": "Thanos",
      "category": 5,
      "difficulty": 3,
      "id": 25,
      "question": "What is the name of the actor that plays Thanos is Avengers"
    }
  ],
  "success": true,
  "total_questions": 20
}
```

**DELETE** /questions/<question_id>

This endpoint deletes a question from the database and takes in the ID of the question to be deleted in the request URL and returns status of the request, the ID of the question that has been deleted and the total number of questions available

_Sample Request_

```bash
# delete a question with the ID of 16
$ curl -X DELETE localhost:5000/questions/16
```

_Sample Response_

```JSON
{
  "deleted": 16,
  "success": true,
  "total_questions": 19
}
```

**POST** /questions

This endpoint creates a new question and takes in some required parameters in the request body. Here are the required parameters:

```JSON
{
  "question": <type:String>, # body of the question
  "answer": <type:String>, #answer to the question
  "category": <type:Integer>, # category ID the question belongs to
  "difficulty": <type:Integer> # a value ranging from 1 - 5 on the difficulty of the question
}
```

_Sample Request_

```bash
$ curl --location --request POST "localhost:5000/questions" \
  --header "Content-Type: application/json" \
  --data "{
        \"question\": \"What is Darth Vader's real name?\",
        \"answer\": \" Anakin Skywalker\",
        \"category\": 1,
        \"difficulty\": 3
}"
```

_Sample Response_

```JSON
{
  "created": 26,
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    ...
  ],
  "success": true,
  "total_questions": 20
}
```

**POST** /questions/search

Hitting this endpoint with a search term in the request body returns a result with all questions that match the given search term. The request requires a single parameter in the body:

```JSON
{
  "searchTerm": <type:String>
}
```

_Sample Request_

```bash
$ curl --location --request POST "localhost:5000/questions/search" \
  --header "Content-Type: application/json" \
  --data "{
        \"searchTerm\": \"who?\",
}"
```

_Sample Response_

```JSON
{
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    }
  ],
  "success": true,
  "total_questions": 4
}
```

**GET** /categories/<category_id>/questions

This endpoint returns all questions for a given category. The ID of the category should be specified in the request URL.

_Sample Request_

```bash
$ curl -X GET localhost:5000/categories/6/questions
```

_Sample Response_

```JSON
{
  "current_category": {
    "id": 6,
    "type": "Sports"
  },
  "questions": [
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }
  ],
  "success": true,
  "total_questions": 2
}
```

**POST** /quizzes

This endpoint gets a random quiz question selected from a particular category or from all categories if a `quiz_cateory` is specified in the request body. It also accepts a `previous_questions` parameter in the request body which is an array of ID's previously selected questions that the API has sent;

```JSON
{
  "quiz_category": <type:Object> {
    "id": <type:Integer>,
    "type": <type:String>
    },
    "previous_questions": <type:Array> [
      <type:Integer>
    ]
}
```

_Sample Request_

```bash
$ curl --location --request POST "localhost:5000/quizzes" \
  --header "Content-Type: application/json" \
  --data "{
        \"quiz_category\": { \"id\": 6, \"type\": \"Sports\" },
        \"previous_questions\": [11]
}"
```

_Sample Response_

```JSON
{
  "question": {
    "answer": "Brazil",
    "category": 6,
    "difficulty": 3,
    "id": 10,
    "question": "Which is the only team to play in every soccer World Cup tournament?"
  },
  "success": true
}
```

#### Errors

Typically, errors might occur during requests. Shown below are the custom error responses for every handled HTTP error.

**400**

```JSON
{
  "success": false,
  "error": 400,
  "message": "bad request, please format and try again"
}
```

**404**

```JSON
{
  "success": false,
  "error": 404,
  "message": "resource not found"
}
```

**405**

```JSON
{
  "success": false,
  "error": 405,
  "message": "method not allowed"
}
```

**422**

```JSON
{
  "success": false,
  "error": 422,
  "message": "unprocessable request"
}
```

**500**

```JSON
{
  "success": false,
  "error": 500,
  "message": "an error occurred on the server please try again"
}
```

## Testing

To run the tests, run

```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
