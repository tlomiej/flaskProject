from flask import render_template, request, jsonify

from mainapp.forms.utils import check_type_json

from flask import Blueprint

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    if check_type_json(request.args.get('type')):
        return jsonify({'title': 'Collect data you want!',
                        'method': ['seeAvailableForm','addForm']})
    return render_template('home.html')


