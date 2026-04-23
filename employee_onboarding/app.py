from flask import Flask, render_template, request, jsonify
from models import db, Employee, Training
from config import Config

app = Flask(__name__)   # create app first

app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/add_employee', methods=['POST'])
def add_employee():
    name = request.form['name']
    email = request.form['email']
    department = request.form['department']

    employee = Employee(
        name=name,
        email=email,
        department=department
    )

    db.session.add(employee)
    db.session.commit()

    return "Employee Added"

@app.route('/add_training', methods=['POST'])
def add_training():
    return jsonify({"message": "Training Added"})

if __name__ == '__main__':
    app.run(debug=True)