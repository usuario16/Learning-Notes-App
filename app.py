# Notas de mi aprendizajes diarios

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_wtf.csrf import CSRFProtect
from flask_wtf import FlaskForm


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/notes.db'
app.config['SECRET_KEY'] = 'secret_key'
app.config['WTF_CSRF_SECRET_KEY'] = 'secret_key'

db = SQLAlchemy(app)

# Protección CSRF
csrf = CSRFProtect(app)
class Token(FlaskForm):
    pass


from models import Note

# Vista de inicio -> LISTO
@app.route('/')
def index():
    notes = Note.query.order_by(Note.id.desc()).all()
    num_notes = len(notes)
    return render_template('index.html', notes=notes, num_notes=num_notes)


# Vista de crear un registro -> LISTO
@app.route('/create', methods=['POST', 'GET'])
def create():
    token = Token()
    if request.method == 'POST':
        title = request.form.get('title')
        topic = request.form.get('topic')
        content = request.form.get('content')
        note = Note(title=title, topic=topic, content=content, done=False, created_at=datetime.now().date())
        db.session.add(note)
        db.session.commit()
        return redirect(url_for('created'))

    return render_template('create.html', token=token)


# Vista de editar un registro
@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    token = Token()
    note = Note.query.filter_by(id=id).first()
    if request.method == 'POST':
        note.title = request.form['title']
        note.topic = request.form['topic']
        note.content = request.form['content']
        
        """
        El input checkbox entrega dos valores:
            - Cuando ha sido cliqueado entrega 'on'
            - Cuando NO ha sido cliqueado entrega 'None
        """

        done_or_not = request.form.get('done')

        print(done_or_not)

        if done_or_not == 'on':
            done_or_not = 1
        else:
            done_or_not = 0

        note.done = done_or_not

        db.session.commit()
        return redirect(url_for('index'))

    return render_template('edit.html', note=note, token=token)

@app.route('/done/<id>')
def done(id):
    note = Note.query.filter_by(id=id).first()
    if note.done == 1:
        note.done = 0
    else:
        note.done = 1
    
    db.session.commit()

    return redirect(url_for('index'))

# Vista de eliminar un registro -> LISTO
@app.route('/delete/<id>')
def delete(id):
    note = Note.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect(url_for('index'))


#####################################################################################################

# VENTANA FLASH 

# Vista de registro completado -> LISTO
@app.route('/created')
def created():
    return render_template('created.html')

