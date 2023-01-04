from datetime import datetime

import flask
from flask import jsonify, request
from flask_migrate import Migrate
from flask_restful import abort
from flask_sqlalchemy import SQLAlchemy
from idna import unicode

app = flask.Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres@localhost/flask_api'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    person = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return '<Post %r>' %self.id

@app.route('/bulboard/api/v1.0/publication/', methods=['GET'])
def get_publications():
    lis = []
    items = Post.query.all()
    for d in items:
        lis.append({"id": d.id, "title": d.title, "description": d.description, "created_on": d.created_on, "person": d.person})
    return jsonify({'tasks': lis})

@app.route('/bulboard/api/v1.0/publication/<int:public_id>', methods=['GET'])
def get_publication(public_id):
    lis = []
    vor = {}
    items = Post.query.get(public_id)
    vor.update(id=items.id, title=items.title, description=items.description, created_on=items.created_on, person=items.person)
    lis.append(vor)
    return jsonify({'tasks': vor})

@app.route('/bulboard/api/v1.0/publication', methods=['POST'])
def create_publication():
    title = request.json.get('title')
    description = request.json.get('description')
    existing_title_descr = Post.query \
        .filter(Post.title == title) \
        .filter(Post.description == description) \
        .one_or_none()
    if existing_title_descr is None:
        p = Post( title=request.json["title"], description=request.json["description"], person=request.json["person"] )
        db.session.add(p)
        db.session.commit()
        return 'Successfully!'
    else:
        return f"title = {request.json['title']} or description = {request.json['description']} already exists!", 409

@app.route('/bulboard/api/v1.0/publication/<int:public_id>', methods=['PUT'])
def update_publication(public_id):
    vor = {}
    if public_id == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    p = Post.query.get(public_id)
    p.title = request.json['title']
    p.description = request.json['description']
    p.person = request.json['person']
    db.session.commit()
    publicid = Post.query.get(public_id)
    vor.update(id=publicid.id, title=publicid.title, description=publicid.description, created_on=publicid.created_on,
               person=publicid.person)
    return jsonify({'task': vor})

@app.route('/bulboard/api/v1.0/publication/<int:public_id>', methods=['DELETE'])
def delete_publication(public_id):
    publicid = Post.query.get(public_id)
    db.session.delete(publicid)
    db.session.commit()
    return 'Successfully!'

if __name__ == '__main__':



 app.run()
