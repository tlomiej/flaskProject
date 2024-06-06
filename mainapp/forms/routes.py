import json


from flask import Blueprint, request, abort, jsonify
from flask_login import login_required,current_user
from mainapp.forms.forms import NewForm, EditForm
from mainapp.forms.utils import create_form_class, combine_data, return_json, check_type_json, return_data
from mainapp import db


from flask import render_template, url_for, flash, redirect

from mainapp.models import Forms, Formsdata

forms = Blueprint('forms', __name__)



@forms.route("/forms", methods=['GET', 'POST'])
def form():
    data = Forms.query.all()
    return return_data(data, request.args.get('type'),
                       render_template('forms.html', title='Forms', data=data))


@forms.route("/newform", methods=['GET', 'POST'])
@login_required
def new_form():
    if check_type_json(request.args.get('type')):
        if request.method == 'GET':
            return jsonify({'message': 'Use POST method!'}), 400

        if request.content_type != 'application/json':
            return jsonify({'message': 'Content-Type must be application/json'}), 415

        try:
            json_data = request.get_json()
            if not json_data or not 'title' in json_data or not 'description' in json_data:
                return jsonify({'message': 'Invalid input'}), 400

            collections = Forms(title=json_data.get('title'), description=json_data.get('description'), form=json_data.get('form'),
                                author=current_user)
            db.session.add(collections)
            db.session.commit()
            return jsonify({'message': 'Add new form'}), 201

        except Exception as e:
            return jsonify({'message': 'Invalid JSON', 'error': str(e)}), 400


    form = NewForm()
    if form.validate_on_submit():
        collections = Forms(title=form.title.data, description=form.description.data, form=form.form.data, author=current_user)
        db.session.add(collections)
        db.session.commit()

        flash('Form created!', 'success')
        return redirect(url_for('forms.form'))
    elif request.method == 'GET':
        form.form.data = '''
        {
            "fields": [
                {"name": "title", "type": "StringField", "label": "Title", "validators": ["DataRequired"]},
                {"name": "content", "type": "TextAreaField", "label": "Content", "validators": ["DataRequired"]},
                {"name": "x", "type": "TextAreaField", "label": "X", "validators": ["DataRequired"]},
                {"name": "y", "type": "TextAreaField", "label": "Y", "validators": ["DataRequired"]}
            ],
            "submit": {"label": "Add"}
        }
        '''

    return render_template('new_form.html', title='Form',legend='New Form', form=form)




@forms.route("/forms/<id>", methods=['GET', 'POST'])
def form_view(id):
    count = Formsdata.query.filter_by(form_id=id).count()
    form = Forms.query.with_entities(Forms.title, Forms.description).filter_by(id=id).first()

    if check_type_json(request.args.get('type')):
        return jsonify({'count': count, 'form': {'title': form.title,
                                                 'description': form.description
        }})
    return render_template('form_root.html', title='Form', form=form, id=id, count=count)


@forms.route("/forms/<id>/new", methods=['GET', 'POST'])
@login_required
def form_add(id):
    if check_type_json(request.args.get('type')):
        if request.method == 'GET':
            return jsonify({'message': 'Use POST method!'}), 400

        if request.content_type != 'application/json':
            return jsonify({'message': 'Content-Type must be application/json'}), 415

        try:
            json_data = request.get_json()
            if not json_data or not 'data' in json_data:
                return jsonify({'message': 'Invalid input'}), 400

            formdata = Formsdata(data=json.dumps(json_data.get('data')), form_id=id, author=current_user)
            db.session.add(formdata)
            db.session.commit()

            return jsonify({'message': f'Add new row in form: {id}'}), 201

        except Exception as e:
            return jsonify({'message': 'Invalid JSON', 'error': str(e)}), 400


    data = Forms.query.filter_by(id=id).first_or_404()
    form_definition = json.loads(data.form.replace("'", '"'))
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

@forms.route("/forms/<id>/edit", methods=['GET', 'POST'])
@login_required
def form_edit(id):
    data = Forms.query.filter_by(id=id).first_or_404()

    if data.author != current_user:
        abort(403)

    form = EditForm()
    if form.validate_on_submit():
        data.title = form.title.data
        data.description = form.description.data
        data.form = form.form.data
        db.session.commit()
        flash('Form updated!', 'success')
        return redirect(url_for('forms.form_view', id=id))

    elif request.method == 'GET':

        form.title.data =  data.title
        form.description.data = data.description
        form.form.data = data.form

    return render_template('new_form.html', title='Form', legend='Edit Form', form=form)
@forms.route("/forms/<id>/delete", methods=['GET', 'POST'])
@login_required
def form_delete(id):
    data = Forms.query.filter_by(id=id).first_or_404()

    if data.author != current_user:
        abort(403)
    db.session.delete(data)
    Formsdata.query.filter_by(form_id=id).delete()
    db.session.commit()
    flash(f'Form has been deleted! [{id}]', 'success')
    return redirect(url_for('forms.form'))

@forms.route("/forms/<id>/table", methods=['GET', 'POST'])
def form_table(id):
    form = Forms.query.filter_by(id=id).first()
    form_data = json.loads(form.form.replace("'", '"'))
    data = Formsdata.query.filter_by(form_id=id).all()

    d = []
    for x in data:
        d.append(combine_data(x.data, form_data['fields']))

    if check_type_json(request.args.get('type')):
        return jsonify({'form': d })
    return render_template('formview.html', title='Form', form=d, id=id)


