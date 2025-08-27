from flask import Flask, render_template, redirect, url_for, request , flash
import mysql.connector
app = Flask(__name__)

count_question = 1
count_no = 1
student_marks = 0

conn =  mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="quiz_database"
)
cursor_obj = conn.cursor()



# Welcome Page
@app.route('/')
def welcome():
    return render_template('welcome.html')

# Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        query = "SELECT id, role FROM user_info WHERE username = %s AND password = %s"
        cursor_obj.execute(query, (username, password))
        user = cursor_obj.fetchone()

        if user:  # login successful
            if user[1].lower() == "teacher":
                return redirect(url_for('teacher_dashboard', teacher_id = user[0]))
            elif user[1].lower() == "student":
                return redirect(url_for('student_dashboard', student_id = user[0]))
            else :
                return render_template('login.html', error="Invalid username or password")
        else:
            return render_template('login.html', error="Invalid username or password")
    return render_template('login.html', error="Invalid username or password")


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        c_password = request.form['confirm_password']
        age = request.form['age']
        gender = request.form['gender']
        dob = request.form['dob']
        role = request.form['role']

        if password != c_password:
            flash("Passwords do not match", "error")
            return redirect(url_for('register_page'))

        max_id_sql = "SELECT MAX(id) FROM user_info"
        insert_user_info = "INSERT INTO user_info (id, username, email, password, age, gender, dob, role) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        cursor_obj.execute(max_id_sql)
        max_id = cursor_obj.fetchone()
        user_id = max_id[0] + 1
        cursor_obj.execute(insert_user_info, (user_id, username, email, password,age,gender, dob, role))
        conn.commit()
        return redirect(url_for('reg_success'))
    return render_template('register.html')

@app.route('/reg_success')
def reg_success():
    return render_template('reg_success.html')

@app.route('/student_dashboard/<student_id>', methods= ['GET','POST'])
def student_dashboard(student_id):
    sql = "select email , age , gender , dob , role, username from user_info where id = %s "
    cursor_obj.execute(sql,(student_id,))
    user = cursor_obj.fetchone()

    if(user):

        email = user[0]
        age = user [1]
        gender = user[2]
        dob = user [3]
        role = user[4]
        student_name = user[5]

    if request.method == 'POST':
        quiz_code = request.form['quiz_code']
        return redirect(url_for('quiz_dashbord', student_id = student_id, quiz_code=quiz_code))

    return render_template('student.html',student_name=f"{student_name}",student_email = f"{email}")

@app.route('/teacher_dashboard/<teacher_id>', methods= ['GET','POST'])
def teacher_dashboard(teacher_id):

    teacher_sql = f"select username, email from user_info where id = {teacher_id} "
    cursor_obj.execute(teacher_sql)
    teacher = cursor_obj.fetchone()
    if teacher:
        teacher_name = teacher[0]
        teacher_email = teacher[1]
    if request.method == 'POST':
        quiz_code = request.form["quiz_code"]
        quiz_name = request.form["quiz_name"]
        quiz_discription = request.form["quiz_discription"]
        max_questions = request.form["max_questions"]
        creator_sql = f"select username from user_info where id = {teacher_id}"
        cursor_obj.execute(creator_sql)
        creator = cursor_obj.fetchone()
        sql1 = """INSERT INTO quiz_info 
          (quiz_code, quiz_name, quiz_discription, max_questions, creator) 
          VALUES (%s, %s, %s, %s, %s)"""
        sql = f"""CREATE TABLE quiz_{quiz_code} (
                question_id INT,
                mark INT,
                question VARCHAR(100),
                correct_answer VARCHAR(100),
                option1 VARCHAR(100),
                option2 VARCHAR(100),
                option3 VARCHAR(100),
                option4 VARCHAR(100))"""
        cursor_obj.execute(sql1, (quiz_code, quiz_name, quiz_discription, max_questions, creator[0]))
        conn.commit()
        cursor_obj.execute(sql)
        return redirect(url_for('create_dashboard', teacher_id = teacher_id, quiz_code=quiz_code, count = count_no))

    return render_template('teacher.html',teacher_name = teacher_name, teacher_email = teacher_email)

@app.route('/create_dashboard/<teacher_id>/<quiz_code>/<count>', methods=['GET', 'POST'])
def create_dashboard(teacher_id,quiz_code,count):
    global count_no

    if request.method == 'POST':
        max_sql = f"SELECT max_questions FROM quiz_info where quiz_code = {quiz_code}"
        cursor_obj.execute(max_sql)
        max = cursor_obj.fetchone()
        print(max[0], count_no)

        count_no += 1


        question_id = request.form['id']
        question = request.form['question']
        mark = request.form['mark']
        option1 = request.form['option1']
        option2 = request.form['option2']
        option3 = request.form['option3']
        option4 = request.form['option4']
        correct_option = request.form['correct_option']

        insert_quiz_info = f"""INSERT INTO quiz_{quiz_code}
    (question_id, mark, question, correct_answer, option1, option2, option3, option4)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        cursor_obj.execute(insert_quiz_info,(question_id, mark, question ,correct_option ,option1 ,option2 ,option3 ,option4))
        conn.commit()
        
        if count_no > max[0]:
            count_no = 1
            return redirect(url_for('reg_success'))
        
        return redirect(url_for('create_dashboard', teacher_id = teacher_id, quiz_code=quiz_code, count = count_no))

    return render_template('create_dashboard.html')

# Quiz Dashboard (example after login)
@app.route('/quiz_dashbord/<student_id>/<quiz_code>', methods=['GET','POST'])
def quiz_dashbord(student_id, quiz_code):
    global count_question
    quiz_info_sql = "select max_questions, quiz_name, quiz_discription, creator from quiz_info where quiz_code = %s"
    cursor_obj.execute(quiz_info_sql,(quiz_code,))
    quiz_info = cursor_obj.fetchone()
    if quiz_info:
        quiz_name = quiz_info[1]
        quiz_max = quiz_info[0]
        quiz_discription = quiz_info[2]
        quiz_creator = quiz_info[3]
    
    max_marks_sql = f"select sum(mark) from quiz_{quiz_code}"
    cursor_obj.execute(max_marks_sql)
    max_marks = cursor_obj.fetchone()

    if request.form.get('start-btn') == 'button1':
        return redirect(url_for('question_dashboard',student_id = student_id, quiz_code=quiz_code, question_no=count_question))

    
    return render_template('quiz_dashbord.html',quiz_code = f"{quiz_code}", quiz_name = f"{quiz_name}", quiz_max = f"{quiz_max}", quiz_discription = f"{quiz_discription}", max_marks = f"{max_marks[0]}", quiz_creator = f"{quiz_creator}")

@app.route('/question_dashboard/<student_id>/<quiz_code>/<question_no>',methods =['GET','POST'])
def question_dashboard(student_id,quiz_code,question_no):
    global count_question,student_marks
    print(question_no)
    quiz_data_sql = f"select mark, question, correct_answer,option1, option2, option3, option4 from quiz_{quiz_code} where question_id = {question_no}"
    cursor_obj.execute(quiz_data_sql)
    quiz_data = cursor_obj.fetchone()
    max_sql = f"select max_questions from quiz_info where quiz_code = {quiz_code}"
    cursor_obj.execute(max_sql)
    max1 = cursor_obj.fetchone()

    if quiz_data:
        mark = quiz_data[0]
        question = quiz_data[1]
        c_answer = quiz_data[2]
        option1 = quiz_data[3]
        option2 = quiz_data[4]
        option3 = quiz_data[5]
        option4 = quiz_data[6]
        max2 = max1[0]
    
    if request.method == 'POST':
        s_answer = request.form['op']
        print(s_answer)
        print(c_answer)
        if c_answer.lower() == s_answer.lower() :
            student_marks = student_marks + mark
        print(student_marks)
        print(count_question)

        count_question = count_question+1

        if count_question > max2:
            count_question = 1
            
            return redirect(url_for('result_dashboard',student_id = student_id, quiz_code=quiz_code,marks = student_marks ))
        

        return redirect(url_for('question_dashboard',student_id = student_id, quiz_code=quiz_code, question_no=count_question))

        
    return render_template('question.html',question = question, mark = mark, option1 = option1, option2= option2, option3 = option3,option4= option4, id = question_no )

@app.route('/result_dashboard/<student_id>/<quiz_code>/<marks>',methods =['GET','POST'])
def result_dashboard(student_id,quiz_code,marks):
    global student_marks
    student_marks=0
    max_sql = f"SELECT SUM(mark) FROM quiz_{quiz_code};"
    cursor_obj.execute(max_sql)
    max = cursor_obj.fetchone()

    insert_marks_sql = "INSERT INTO result_info (student_id, quiz_code, total_marks, student_score) VALUES (%s, %s, %s, %s)"
    cursor_obj.execute(insert_marks_sql, (student_id,quiz_code, max[0], marks ))
    conn.commit()
    if request.form.get('back-btn') == 'button':
        return redirect(url_for('student_dashboard',student_id = student_id))
    return render_template('result.html',student_marks = marks,total_marks = max[0] )

if __name__ == '__main__':
    app.run(debug=True)
