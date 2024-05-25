import json

from flask import Blueprint
from flask_login import login_required,current_user
from mainapp.forms.forms import NewForm
from mainapp.forms.utils import create_form_class, combine_data
from mainapp import db


from flask import render_template, url_for, flash, redirect

from mainapp.models import Forms, Formsdata

forms = Blueprint('forms', __name__)

@forms.route("/forms", methods=['GET', 'POST'])
def form():
    data = Forms.query.all()
    return render_template('forms.html', title='Forms', data=data)

@forms.route("/newform", methods=['GET', 'POST'])
@login_required
def new_form():
    form = NewForm()

    form.form.data = '''
    {
        "fields": [
            {"name": "title", "type": "StringField", "label": "Title 1666", "validators": ["DataRequired"]},
            {"name": "content", "type": "TextAreaField", "label": "Content1666", "validators": ["DataRequired"]},
            {"name": "x", "type": "TextAreaField", "label": "X", "validators": ["DataRequired"]},
            {"name": "y", "type": "TextAreaField", "label": "Y", "validators": ["DataRequired"]}
        ],
        "submit": {"label": "Add"}
    }
    '''


    if form.validate_on_submit():
        collections = Forms(title=form.title.data, description=form.form.description, form=form.form.data, author=current_user)
        db.session.add(collections)
        db.session.commit()

        flash('Form created!', 'success')
        return redirect(url_for('forms.form'))

    return render_template('new_form.html', title='Form', form=form)




@forms.route("/forms/<id>", methods=['GET', 'POST'])
def form_view(id):
    count = Formsdata.query.filter_by(form_id=id).count()
    return render_template('form_root.html', title='Form', id=id, count=count)


@forms.route("/forms/<id>/new", methods=['GET', 'POST'])
@login_required
def form_add(id):
    data = Forms.query.filter_by(id=id).first_or_404()
    form_definition = json.loads(data.form)
    dynamicForm = create_form_class(form_definition)
    form = dynamicForm()


    if form.validate_on_submit():
        form_data = {field.name: field.data for field in form if field.name not in ('csrf_token', 'submit') }
        form_data_json = json.dumps(form_data)

        formdata = Formsdata(data=form_data_json, form_id=id, author=current_user)
        db.session.add(formdata)
        db.session.commit()

        flash('Data add to db!', 'success')
        return redirect(url_for('forms.form_view', id=id))
    return render_template('form.html', title='Form', form=form, form_config=form_definition)


@forms.route("/forms/<id>/table", methods=['GET', 'POST'])
def form_table(id):
    form = Forms.query.filter_by(id=id).first()
    form_data = json.loads(form.form)
    data = Formsdata.query.filter_by(form_id=id).all()

    d = []
    for x in data:
        d.append(combine_data(x.data, form_data['fields']))
    return render_template('formview.html', title='Form', form=d)


