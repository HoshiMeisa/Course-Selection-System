class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def check_password(self, password):
        return self.password == password

class Admin(User):
    def __init__(self, username, password):
        super().__init__(username, password)

class Student(User):
    def __init__(self, major, grade, student_id, name, username, password):
        super().__init__(username, password)
        self.major = major
        self.grade = grade
        self.student_id = student_id
        self.name = name

    def __str__(self):
        return f"{self.name} (学号: {self.student_id}, 年级: {self.grade}, 专业: {self.major})"

class LabCourse:
    def __init__(self, course_id, course_name, credits, max_students, instructor, target_grade, location):
        self.course_id = course_id
        self.course_name = course_name
        self.credits = credits
        self.max_students = max_students
        self.instructor = instructor
        self.target_grade = target_grade
        self.location = location
        self.students = []

    def add_student(self, student):
        if len(self.students) >= self.max_students:
            print(f"{self.course_name} 选课人数已满，不能再选课。")
            return False
        if student in self.students:
            print(f"{student.name} 已经选了这门课程。")
            return False
        self.students.append(student)
        return True

    def __str__(self):
        return f"{self.course_name} (课程编号: {self.course_id}, 学分: {self.credits}, 人数上限: {self.max_students}, 授课教师: {self.instructor}, 开课年级: {self.target_grade}, 上课地点: {self.location})"

class CourseSelection:
    def __init__(self):
        self.selections = []

    def add_selection(self, student, lab_course):
        if lab_course.add_student(student):
            self.selections.append((student, lab_course))
            print(f"{student.name} 成功选课 {lab_course.course_name}。")
        else:
            print(f"{student.name} 选课 {lab_course.course_name} 失败。")

    def display_selections(self):
        for student, lab_course in self.selections:
            print(f"{student} 选课 {lab_course.course_name}")

    def find_selections_by_course_name(self, course_name):
        return [(student, lab_course) for student, lab_course in self.selections if lab_course.course_name == course_name]

    def find_selections_by_student_name(self, student_name):
        return [(student, lab_course) for student, lab_course in self.selections if student.name == student_name]