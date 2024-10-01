from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Define the Todo model
class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

# Define the route for the homepage
@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
        return redirect('/view_todos')  # Redirect to view_todos after adding
    return render_template('index.html')

@app.route('/view_todos')
def view_todos():
    allTodo = Todo.query.all()  # Fetch all todos from the database
    return render_template('view_todos.html', allTodo=allTodo)



@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')  # Get the search query from the URL
    allTodo = Todo.query.filter(Todo.title.contains(query) | Todo.desc.contains(query)).all()  # Search todos
    return render_template('view_todos.html', allTodo=allTodo, search_query=query)  # Render the todos with the search results




@app.route('/show')
def show_products():
    allTodo = Todo.query.all()
    print(allTodo)
    return 'All todos are here'


@app.route('/update/<int:sno>', methods=['GET','POST'])
def update(sno):
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc=desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/view_todos")
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo)

@app.route('/delete/<int:sno>')
def delete(sno):
    alltodo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(alltodo)
    db.session.commit()
    return redirect("/")

@app.route('/about')
def about():
    return render_template('about.html')


# Main entry point
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create the database tables before running the app
    app.run(debug=True)
