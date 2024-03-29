from flask import Flask, render_template, request, redirect
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
db=SQLAlchemy(app)

#creting the schema of our database
class Todo(db.Model):
    date_time = datetime.now()
    sno=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(200),nullable=False)
    desc=db.Column(db.String(1000),nullable=False)
    date=db.Column(db.String,default=date_time.strftime("%d/%m/%Y "))
    time=db.Column(db.String,default=date_time.strftime("%I:%M   %p"))

    #display the details of our code
    def __repr__(self)->str:
        return f"{self.sno} {self.title}"

#our homepage
@app.route("/",methods=['GET','POST'])
def hello_world():
    if request.method=='POST':
            title=request.form['title']
            desc=request.form['desc']
            todo=Todo(title=title,desc=desc)
            db.session.add(todo)
            db.session.commit()

    mytodo=Todo.query.all()
    return render_template('index.html',mytodo=mytodo)

#delete todos 
@app.route("/delete/<int:sno>")
def delete(sno):
    todo=Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    mytodo=Todo.query.all()
    return redirect('/')
    # return 'Deleteed'

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/privacy and policy')
def privacy():
    return render_template('privacy.html')

@app.route('/update/<int:sno>',methods=['GET','POST'])
def update(sno):
    if request.method=='POST':
        title=request.form['title']
        desc=request.form['desc']
        todo=Todo.query.filter_by(sno=sno).first()
        todo.title=title
        todo.desc=desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    todo=Todo.query.filter_by(sno=sno).first()
    return render_template('update.html',todo=todo)

if __name__=='__main__':
    app.run(debug=True)