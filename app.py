from flask import Flask, render_template, request, redirect, url_for, flash, session
from course_management import Admin, Student, LabCourse, CourseSelection

app = Flask(__name__)
app.secret_key = "your_secret_key"

# 初始化数据
students = [
    # 在这里添加至少 10 个学生
]
courses = [
    # 在这里添加至少 5 个实验课程（见上面的示例数据）
]
course_selection = CourseSelection()

admins = [
    # 在这里添加至少一个管理员账号
]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        role = request.form["role"]

        if role == "student":
            student = next((s for s in students if s.username == username), None)
            if student is not None and student.check_password(password):
                session["user"] = {"type": "student", "id": student.student_id}
                return redirect(url_for("student_courses"))
        elif role == "admin":
            admin = next((a for a in admins if a.username == username), None)
            if admin is not None and admin.check_password(password):
                session["user"] = {"type": "admin"}
                return redirect(url_for("admin_students"))

        flash("用户名或密码错误，请重试")
    return render_template("login.html")

# 其他路由和函数定义

@app.route("/student/courses")
def student_courses():
    if session["user"]["type"] != "student":
        return redirect(url_for("index"))
    return render_template("student_courses.html", courses=courses)

@app.route("/student/selected_courses")
def student_selected_courses():
    if session["user"]["type"] != "student":
        return redirect(url_for("index"))
    student_id = session["user"]["id"]
    student = next(s for s in students if s.student_id == student_id)
    selected_courses = course_selection.find_selections_by_student_name(student.name)
    return render_template("student_selected_courses.html", courses=[c[1] for c in selected_courses])

@app.route("/student/select_course/<course_id>")
def select_course(course_id):
    if session["user"]["type"] != "student":
        return redirect(url_for("index"))
    student_id = session["user"]["id"]
    student = next(s for s in students if s.student_id == student_id)
    lab_course = next((c for c in courses if c.course_id == course_id), None)
    if lab_course:
        course_selection.add_selection(student, lab_course)
        flash(f"选课 {lab_course.course_name} 成功！")
    return redirect(url_for("student_courses"))

@app.route("/student/drop_course/<course_id>")
def drop_course(course_id):
    if session["user"]["type"] != "student":
        return redirect(url_for("index"))
    student_id = session["user"]["id"]
    student = next(s for s in students if s.student_id == student_id)
    lab_course = next((c for c in courses if c.course_id == course_id), None)
    if lab_course and lab_course in student.selected_courses:
        student.selected_courses.remove(lab_course)
        flash(f"退课 {lab_course.course_name} 成功！")
    return redirect(url_for("student_selected_courses"))

if __name__ == "__main__":
    app.run(debug=True)