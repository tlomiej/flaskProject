from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
import json
import copy


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

    # Add submit field
    setattr(DynamicForm, 'submit', SubmitField(form_definition['submit']['label']))

    return DynamicForm


def combine_data(x, m):
    xj = json.loads(x)
    for z in m:
        z['value'] = xj.get(z['name'])
    return copy.deepcopy(m)