from flask import Flask, render_template, request, redirect, url_for, flash
from course_management import Student, LabCourse, CourseSelection

app = Flask(__name__)
app.secret_key = "your_secret_key"

# 初始化数据
students = [
    # 在这里添加至少 10 个学生
]
courses = [
    # 在这里添加至少 5 个实验课程
]
course_selection = CourseSelection()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # 在这里实现登录逻辑，例如检查用户名和密码
        return redirect(url_for("index"))
    return render_template("login.html")

@app.route("/admin/students")
def admin_students():
    return render_template("admin_students.html", students=students)

@app.route("/admin/courses")
def admin_courses():
    return render_template("admin_courses.html", courses=courses)

@app.route("/student/courses")
def student_courses():
    return render_template("student_courses.html", courses=courses)

@app.route("/student/selected_courses")
def student_selected_courses():
    # 在这里实现获取当前登录学生的选课信息
    selected_courses = []
    return render_template("student_selected_courses.html", courses=selected_courses)

if __name__ == "__main__":
    app.run(debug=True)