from flask import Flask,request, make_response
from flask_migrate import Migrate
from models import db, User
from flask_restful import Api, Resource

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///flask.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION']=False
app.json.compact = False

migrate = Migrate(app,db)
db.init_app(app)
api= Api(app)

@app.route('/')
def index():
    header = '<h1>This is the first page</h1>'
    return header

@app.route('/users',methods=['GET','POST'])
def users():
    if request.method == 'GET':
        users = [user.to_dict() for user in User.query.all()]
        response = make_response(
            users,
            200
        )
        return response
    elif request.method == 'POST':
        new_user = User(
            name= request.form.get('name')
        )
        db.session.add(new_user)
        db.session.commit()
        user_dict = new_user.to_dict()
        response= make_response(
            user_dict,
            201
        )
        return response
@app.route('/users/<int:id>',methods=['GET','DELETE','PATCH'])
def single_users(id):
    user = User.query.filter_by(id=id).first()
    if request.method == 'GET':
        if user:
            body=user.to_dict()
            status = 200
        else:
            body =  {
                "error" : f'The user with {id} does not exist'
            }
            status = 404
        return response
    elif request.method == 'DELETE':
        db.session.delete(user)
        db.session.commit()
        message={
            "message":"user deleted successfully"
        }
        response = make_response(
            message,
            200
        )
        return response

    elif request.method == 'PATCH':
        for attr in request.form:
            setattr(review, attr, request.form.get(attr))

        db.session.add(review)
        db.session.commit()

        review_dict = review.to_dict()

        response = make_response(
            review_dict,
            200
        )

        return response
   
if __name__ == '__main__':
    app.run(port=8000,debug=True)