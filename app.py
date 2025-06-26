from flask import Flask, render_template

import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///events.db'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
db = SQLAlchemy(app)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    date = db.Column(db.String(50))
    image = db.Column(db.String(100))


@app.route('/')
def index():
    events = Event.query.order_by(Event.id.desc()).all()
    return render_template('index.html', events=events)

@app.route('/home')
def home():
    return render_template(index)


@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/gallery')
def gallery():
    return render_template("gallery.html")

@app.route('/team')
def team():
    return render_template("team.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/donate')
def donate():
    return render_template("donate.html")

@app.route('/sewa')
def sewa():
    return render_template('sewa.html')

@app.route('/add-event', methods=['GET', 'POST'])
def add_event():
    if request.method == 'POST':
        name = request.form['name']
        date = request.form['date']
        image = request.files['image']

        image_filename = image.filename
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))

        new_event = Event(name=name, date=date, image=image_filename)
        db.session.add(new_event)
        db.session.commit()
        return redirect(url_for('add_event'))

    events = Event.query.order_by(Event.id.desc()).all()
    return render_template('add_event.html', events=events)


@app.route('/delete-event/<int:id>', methods=['POST'])
def delete_event(id):
    event = Event.query.get_or_404(id)
    
    # Delete the uploaded image file too (optional)
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], event.image)
    if os.path.exists(image_path):
        os.remove(image_path)

    db.session.delete(event)
    db.session.commit()
    return redirect(url_for('add_event'))


# Add more routes as needed...

if __name__ == '__main__':
    app.run(debug=True)
