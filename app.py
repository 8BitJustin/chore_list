from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, time

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class Chore(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_due = db.Column(db.String(), server_default="TESTING")
    content = db.Column(db.String(30), nullable=False)
    date_created = db.Column(db.DateTime,
                             default=datetime.utcnow())

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        chore_content = request.form['content']
        chore_due = request.form['due_date']
        if chore_due == '':
            chore_due = 'None';
        new_chore = Chore(date_due=chore_due, content=chore_content)
        try:
            db.session.add(new_chore)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your chore'
    else:
        chores = Chore.query.order_by(Chore.date_created).all()
        return render_template('index.html', chores=chores)


@app.route('/delete/<int:id>')
def delete(id):
    task_delete = Chore.query.get_or_404(id)

    try:
        db.session.delete(task_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem with deleting the task'


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    chore = Chore.query.get_or_404(id)
    if request.method == 'POST':
        chore.content = request.form['content']
        chore.date_due = request.form['due_date']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was a problem updating your chore'
    else:
        return render_template('update.html', chore=chore)


if __name__ == "__main__":
    app.run(debug=True)