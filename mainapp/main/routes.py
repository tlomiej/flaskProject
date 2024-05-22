from flask import render_template, request
from mainapp.models import User, Collection







from flask import Blueprint

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    data = Collection.query.order_by(Collection.date_created.desc()).paginate(page=page, per_page=5)

    #data = Collection.query.paginate(page=page, per_page=5)
    return render_template('home.html', posts=data)


