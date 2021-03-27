from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

#telling our app where the db is located
#using sqlite for simplicity 
#/// is a relative path, //// is an absolute path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
#intialize db
db = SQLAlchemy(app)

#making a database model for Todo Entries
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    #cannot be null
    content = db.Column(db.String(250), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        #return Task #ID
        return '<Task %r>' % self.id


#This route can GET and POST
@app.route('/', methods = ['POST', 'GET'])
def index():
    #if POST
    if request.method == 'POST':
        #id content for the form in index.html
        task_content = request.form['content']
        #create todo object with its content equal to task_content
        new_task = Todo(content = task_content)
        try:
            #add to db
            db.session.add(new_task)
            #transactional command used to save changes invoked by a transaction to the database
            db.session.commit()
            return redirect('/')
        except:
            return 'Issue Saving to DB'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        #tasks = tasks is the name of the objects which we can use in the HTML
        return render_template('index.html', tasks = tasks)

@app.route('/delete/<int:id>')
def delete(id):
    #get the todo/task of a particular id
    task_delete = Todo.query.get_or_404(id)
    try:
        #delete said task
        db.session.delete(task_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an issue deleting that task'

@app.route('/update/<int:id>', methods = ['POST', 'GET'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating'

    else: 
        return render_template('update.html', task = task)

if __name__ == '__main__':
    app.run(debug=True)