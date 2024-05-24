import json

from flask import Blueprint

from flask import render_template

from mainapp.forms.utils import create_form_class


from flask import render_template, url_for, flash, redirect

from mainapp.models import Forms

forms = Blueprint('forms', __name__)


@forms.route("/forms", methods=['GET', 'POST'])
def form():
    data = Forms.query.all()
    return render_template('forms.html', title='Forms', data=data)



@forms.route("/forms/<id>", methods=['GET', 'POST'])
def form_view(id):
    #TODO find form by id
    return render_template('form_root.html', title='Form')


@forms.route("/forms/<id>/new", methods=['GET', 'POST'])
def form_add(id):

    form_config = '''
    {
        "fields": [
            {"name": "title", "type": "StringField", "label": "Title 11", "validators": ["DataRequired"]},
            {"name": "content", "type": "TextAreaField", "label": "Content1", "validators": ["DataRequired"]},
            {"name": "content2", "type": "TextAreaField", "label": "Content2", "validators": ["DataRequired"]},
            {"name": "content3", "type": "TextAreaField", "label": "Content3", "validators": ["DataRequired"]}
        ],
        "submit": {"label": "Add +"}
    }
    '''
    form_definition = json.loads(form_config)
    dynamicForm = create_form_class(form_definition)
    form = dynamicForm()

    if form.validate_on_submit():


        flash('Add data', 'success')
        return redirect(url_for('forms.form_view', id=id))

    return render_template('form.html', title='Form', form=form, form_config=form_definition)

