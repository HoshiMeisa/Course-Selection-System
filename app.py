from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user

app = Flask(__name__)
app.secret_key = 'supersecretkey'
login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


@app.route('template')
def home():
    return render_template("index.html")


@app.route('/login', methods=['POST'])
def login():
    user_id = request.form['user_id']
    role = request.form['role']
    user = User(user_id)
    login_user(user)
    if role == 'student':
        return redirect(url_for('student'))
    elif role == 'admin':
        return redirect(url_for('admin'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/student')
@login_required
def student():
    return render_template("student.html")


@app.route('/admin')
@login_required
def admin():
    return render_template("admin.html")


if __name__ == "__main__":
    app.run(debug=True)
