from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class Chore(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(30), nullable=False)
    date_created = db.Column(db.DateTime,
                             default=datetime.now())

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        chore_content = request.form['content']
        new_chore = Chore(content=chore_content)

        try:
            db.session.add(new_chore)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your chore'
    else:
        chores = Chore.query.order_by(Chore.date_created).all()
        return render_template('index.html', chores=chores)


if __name__ == "__main__":
    app.run(debug=True)