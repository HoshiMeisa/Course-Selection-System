import json
from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = 'some_secret_key'


def load_credentials(filename):
    with open(filename, 'r') as f:
        return json.load(f)


def load_courses(filename):
    with open(filename, 'r') as f:
        return json.load(f)


def save_courses(filename, courses):
    with open(filename, 'w') as f:
        json.dump(courses, f)


students = load_credentials('students.json')
admins = load_credentials('admins.json')
courses = load_courses('courses.json')


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    user_type = request.form['user_type']
    username = request.form['username']
    password = request.form['password']

    if user_type == 'student':
        if username in students and students[username] == password:
            session['username'] = username
            session['user_type'] = 'student'
            return redirect(url_for('student'))
    elif user_type == 'admin':
        if username in admins and admins[username] == password:
            session['username'] = username
            session['user_type'] = 'admin'
            return redirect(url_for('admin'))

    flash('无效的用户名或密码，请重试。')
    return redirect(url_for('home'))


@app.route('/student')
def student():
    if 'username' not in session or session['user_type'] != 'student':
        return redirect(url_for('home'))
    registered_courses = [course for course in courses.values() if session['username'] in course['students']]
    return render_template('student.html', courses=courses.values(), registered_courses=registered_courses)


@app.route('/admin')
def admin():
    if 'username' not in session or session['user_type'] != 'admin':
        return redirect(url_for('home'))
    return render_template('admin.html', students=students.keys(), courses=courses.values())


@app.route('/admin_drop_course', methods=['POST'])
def admin_drop_course():
    course_id = request.form['course_id']
    student = request.form['student']
    for course_key, course in courses.items():
        if course['course_id'] == course_id:
            if student in course['students']:
                course['students'].remove(student)
                save_courses('courses.json', courses)
                flash(f"已为学生 {student} 退课: {course['course_name']}")
            else:
                flash(f"学生 {student} 未选该课程，无法退课: {course['course_name']}")

    return redirect(url_for('admin'))


@app.route('/register_course', methods=['POST'])
def register_course():
    course_id = request.form['course_id']
    for course_key, course in courses.items():
        if course['course_id'] == course_id:
            if len(course['students']) < course['capacity']:
                if session['username'] not in course['students']:
                    course['students'].append(session['username'])
                    save_courses('courses.json', courses)
                    flash(f"成功选课: {course['course_name']}")
                else:
                    flash(f"已经选过这门课程: {course['course_name']}")
            else:
                flash(f"选课失败，课程已满: {course['course_name']}")

    if session['user_type'] == 'student':
        return redirect(url_for('student'))
    else:
        return redirect(url_for('admin'))


@app.route('/drop_course', methods=['POST'])
def drop_course():
    course_id = request.form['course_id']
    for course_key, course in courses.items():
        if course['course_id'] == course_id:
            if session['username'] in course['students']:
                course['students'].remove(session['username'])
                save_courses('courses.json', courses)
                flash(f"成功退课: {course['course_name']}")
            else:
                flash(f"未选该课程，无法退课: {course['course_name']}")

    if session['user_type'] == 'student':
        return redirect(url_for('student'))
    else:
        return redirect(url_for('admin'))

@app.route('/admin_add_course', methods=['POST'])
def admin_add_course():
    course_id = request.form['course_id']
    course_name = request.form['course_name']

    # Check if the course already exists
    course = Course.query.filter_by(course_id=course_id).first()
    if course:
        flash("课程已存在。")
    else:
        new_course = Course(course_id=course_id, course_name=course_name)
        db.session.add(new_course)
        db.session.commit()
        flash("课程已成功添加。")

    return redirect(url_for('admin'))

@app.route('/admin_delete_course', methods=['POST'])
def admin_delete_course():
    course_id = request.form['course_id']

    # Find the course and delete it
    course = Course.query.filter_by(course_id=course_id).first()
    if course:
        db.session.delete(course)
        db.session.commit()
        flash("课程已成功删除。")
    else:
        flash("课程未找到。")

    return redirect(url_for('admin'))


if __name__ == '__main__':
    app.run(debug=True)
