from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, RadioField
from wtforms.validators import DataRequired
import json
import copy
from flask import request, jsonify


def create_form_class(form_definition):
    class DynamicForm(FlaskForm):
        pass

    for field in form_definition['fields']:
        field_type = field['type']
        field_name = field['name']
        field_label = field['label']

        field_validators = [DataRequired() if v == "DataRequired" else None for v in field['validators']]
        field_validators = [v for v in field_validators if v is not None]

        # Dynamically add fields to the form class
        if field_type == "StringField":
            setattr(DynamicForm, field_name, StringField(field_label, validators=field_validators))
        elif field_type == "TextAreaField":
            setattr(DynamicForm, field_name, TextAreaField(field_label, validators=field_validators))
        elif field_type == "RadioField":
            data_str = field['choices']
            field_choices = [tuple(x) for x in data_str]
            setattr(DynamicForm, field_name, RadioField(field_label, validators=field_validators, choices=field_choices))


    # Add submit field
    setattr(DynamicForm, 'submit', SubmitField(form_definition['submit']['label']))

    return DynamicForm


def combine_data(x, m):
    xj = json.loads(x)
    for z in m:
        z['value'] = xj.get(z['name'])
    return copy.deepcopy(m)


def check_type_json(type):
    if type and type.upper() == 'JSON':
        return True
    else:
        return False


def return_json(data):
    return jsonify([user.to_dict() for user in data])


def return_data(data, type, render):
    if check_type_json(type):
        return return_json(data)
    return render
