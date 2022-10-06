from flask import Flask, request, Response, jsonify, make_response
import psycopg2
import json
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS, cross_origin

DATABASE_URL = ''


def sign_in(email, password):
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        fetch_sql = 'SELECT to_json(users) FROM users where email = \'{email}\''.format(email = email)
        cur.execute(fetch_sql)
        row = cur.fetchone()
        
        conn.commit()
        cur.close()
        
        if row == None:
            return "Account does not exist", None
        if(check_password_hash(row[0]['password'], password)):
            return "Sign in succesful", row
        else:
            return "Password incorrect", None

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            
            
def sign_up(first_name, last_name, email, password):
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        fetch_sql = 'SELECT * FROM users where email = \'{email}\''.format(email = email)
        cur.execute(fetch_sql)
        row = cur.fetchall()
        if len(row) != 0:
            return "Account exists", None
        
        password=generate_password_hash(password, method='sha256')
        insert_sql = 'insert into users(first_name, last_name, email,password) values (\'{first_name}\', \'{last_name}\', \'{email}\', \'{password}\') returning to_json(users)'.format(first_name = first_name, last_name = last_name, email = email, password = password)
        cur.execute(insert_sql)
        
        data = cur.fetchall()
        result = cur.rowcount 
        
        conn.commit()
        cur.close()
        
        if(result == 1):
            return("Succesfully created", data)
        else:
            return("Could not create user", None)
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            
def fetch_questions():
    conn = None
    questions = []
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        
        fetch_sql = 'SELECT to_json(questions) FROM questions'
      
        cur.execute(fetch_sql)
        result = cur.fetchall()
    
        
        for r in result:
            questions.append(r[0])
        
    
        conn.commit()
        cur.close()
        
        
        if len(questions) == 0:
            return "No questions yet", None
        else:
            return "Fetched questions", questions
        

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            

def fetch_feedback():
    conn = None
    feedback = []
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        fetch_sql = 'SELECT to_json(feedbacks) FROM feedbacks'
        cur.execute(fetch_sql)
        result = cur.fetchall()
        for r in result:
            feedback.append(r[0])       
        conn.commit()
        cur.close()
        if len(feedback) == 0:
            return "No feedback yet", None
        else:
            return "Fetched feedback", feedback
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            
def post_feedback(feedback):
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
    
        insert_sql = 'insert into feedbacks(feedback) values ( \'{feedback}\')'.format(feedback = feedback)
        cur.execute(insert_sql)
     
        result = cur.rowcount 
        
        conn.commit()
        cur.close()
        
        if(result == 1):
            return("Feedback succesfully sent")
        else:
            return("Could not post feedback")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
        


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/")
def hello():
    return "<p>TEST - This is an Amharic chatbot.</p>"

@app.route("/signin", methods=['POST'])
def signIn():
    if(request.data and request.json):
        req = request.json
        if('email' in req.keys() and 'password' in req.keys()):
            result, data = sign_in(req['email'].lower(), req['password'])
            if(result=="Sign in succesful"):
                return make_response(jsonify(data[0]), 200)
            if(result=="Account does not exist" or result=="Password incorrect"):
                data = {'message': 'Account non-existant or incorrect login'}
                return make_response(jsonify(data), 400)
            else:
                data = {'message': 'Could not sign in'}
                return make_response(jsonify(data), 500)
        else:
            data = {'message': 'All fields are required'}
            return make_response(jsonify(data), 400)
            
    else:
        data = {'message': 'All fields are required'}
        return make_response(jsonify(data), 400)

    
@app.route("/signup", methods=['POST'])
def signUp():
    if(request.data and request.json):
        req = request.json
        if('email' in req.keys() and 'password' in req.keys() and 'first_name' in req.keys() and 'last_name' in req.keys()):
            result, data = sign_up(req['first_name'], req['last_name'],req['email'].lower(), req['password'])
            if(result=="Succesfully created"):
                return make_response(jsonify(data), 200)
            if(result=="Account exists"):
                data = {'message': 'Account already exists'}
                return make_response(jsonify(data), 400)
            else:
                data = {'message': 'Could not create user'}
                return make_response(jsonify(data), 500)
        else:
            data = {'message': 'All fields are required'}
            return make_response(jsonify(data), 400)
    else:
        data = {'message': 'All fields are required'}
        return make_response(jsonify(data), 400)
        
@app.route("/getquestions", methods=['GET'])
def getQuestions():
    result, data = fetch_questions()
    if result == "No questions yet":
        return make_response(jsonify({'message': 'No questions yet'}), 200)
    elif result == "Fetched questions": 
        return make_response(jsonify(data), 200)
    else:
        return make_response(jsonify({'message': 'Could not fetch questions'}), 500)
    
    
@app.route("/getfeedback", methods=['GET'])
def getFeedback():
    result, data = fetch_feedback()
    if result == "No feedback yet":
        return make_response(jsonify({'message': 'No feedback yet'}), 200)
    elif result == "Fetched feedback":
        return make_response(jsonify(data), 200)
    else:
        return make_response(jsonify({'message': 'Could not fetch feedback'}), 500)


@app.route("/postfeedback", methods=['POST'])
def postFeedback():
    if(request.data and request.json):
        req = request.json
        if('feedback' in req.keys()):
            result = post_feedback(req['feedback'])
            if(result=="Feedback succesfully sent"):
                data = {'message': 'Feedback sent'}
                return make_response(jsonify(data), 200)
            else:
                data = {'message': 'Could not send feedback'}
                return make_response(jsonify(data), 500)
        else:
            data = {'message': 'Missing field'}
            return make_response(jsonify(data), 400)
    else:
        data = {'message': 'Missing field'}
        return make_response(jsonify(data), 400)        
        
@app.route("/savequestion", methods=['POST'])
def saveQuestion():  
    if(request.data and request.json):
        req = request.json
        if('question' in req.keys()):
            conn = None
            result = None
            try:
                conn = psycopg2.connect(DATABASE_URL, sslmode='require')
                cur = conn.cursor()
                insert_sql = 'insert into questions(question) values(\'{question}\') returning question_id'.format(question = req['question'])
                cur.execute(insert_sql)
                result = cur.fetchone()
                conn.commit()
                cur.close()
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
            finally:
                if conn is not None:
                    conn.close()
            data = {'question_id': result[0]}
            return make_response(jsonify(data), 200)
        else:
            data = {'message': 'Missing field'}
            return make_response(jsonify(data), 400)
    else:
        data = {'message': 'Missing field'}
        return make_response(jsonify(data), 400)


@app.route("/updatequestionstate", methods=['PUT'])
def updateQuestionState():  
    if(request.data and request.json):
        req = request.json
        if('resolved' in req.keys() and 'question_id' in req.keys()):
            conn = None
            try:
                conn = psycopg2.connect(DATABASE_URL, sslmode='require')
                cur = conn.cursor()
                update_sql = 'update questions SET resolved = (\'{resolved}\') where question_id = (\'{question_id}\')'.format(resolved = req['resolved'], question_id = req['question_id'])
                cur.execute(update_sql)
                conn.commit()
                cur.close()
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
            finally:
                if conn is not None:
                    conn.close()
            data = {'message': 'Question updated'}
            return make_response(jsonify(data), 200)
        else:
            data = {'message': 'Missing field'}
            return make_response(jsonify(data), 400)
    else:
        data = {'message': 'Missing field'}
        return make_response(jsonify(data), 400)


@app.route("/updatefeedbackstate", methods=['PUT'])
def updateFeedbackState():  
    if(request.data and request.json):
        req = request.json
        if('resolved' in req.keys() and 'feedback_id' in req.keys()):
            conn = None
            try:
                conn = psycopg2.connect(DATABASE_URL, sslmode='require')
                cur = conn.cursor()
                update_sql = 'update feedbacks SET resolved = (\'{resolved}\') where feedback_id = (\'{feedback_id}\')'.format(resolved = req['resolved'], feedback_id = req['feedback_id'])
                cur.execute(update_sql)
                conn.commit()
                cur.close()
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
            finally:
                if conn is not None:
                    conn.close()
            data = {'message': 'Feedback updated'}
            return make_response(jsonify(data), 200)
        else:
            data = {'message': 'Missing field'}
            return make_response(jsonify(data), 400)
    else:
        data = {'message': 'Missing field'}
        return make_response(jsonify(data), 400)



@app.route("/assessanswer", methods=['POST'])
def assessAnswer():  
    if(request.data and request.json):
        req = request.json
        if('resolved' in req.keys()):
            conn = None
            try:
                conn = psycopg2.connect(DATABASE_URL, sslmode='require')
                cur = conn.cursor()
                insert_sql = 'insert into question_stats(resolved) values(\'{resolved}\')'.format(resolved = req['resolved'])
                cur.execute(insert_sql)
                conn.commit()
                cur.close()
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
            finally:
                if conn is not None:
                    conn.close()
            data = {'message': 'Saved assesment'}
            return make_response(jsonify(data), 200)
        else:
            data = {'message': 'Missing field'}
            return make_response(jsonify(data), 400)
    else:
        data = {'message': 'Missing field'}
        return make_response(jsonify(data), 400)


@app.route("/getanswerassesments", methods=['GET'])
def getAnswerAssesments():
    conn = None
    assesments = []
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        fetch_sql = 'SELECT to_json(question_stats) FROM question_stats'
        cur.execute(fetch_sql)
        result = cur.fetchall()
        for r in result:
            assesments.append(r[0])       
        conn.commit()
        cur.close()
        if len(assesments) == 0:
            return make_response(jsonify({'message': 'No data yet'}), 200)
        else:
            return make_response(jsonify(assesments), 200)
    except (Exception, psycopg2.DatabaseError) as error:
        return make_response(jsonify({'message': 'Could not fetch data'}), 500)
    finally:
        if conn is not None:
            conn.close()
