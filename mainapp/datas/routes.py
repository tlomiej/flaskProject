import bcrypt
import os
from flask import render_template, url_for, flash, redirect, request, abort
from mainapp import db
from mainapp.models import User, Collection
from mainapp.datas.forms import NewDataForm
from flask_login import current_user, login_required


from flask import Blueprint

datas = Blueprint('datas', __name__)

@datas.route("/data")
def data():
    page = request.args.get('page', 1, type=int)
    data = Collection.query.order_by(Collection.date_created.desc()).paginate(page=page, per_page=5)

    #data = Collection.query.paginate(page=page, per_page=5)
    return render_template('data.html', posts=data)




@datas.route("/data/new", methods=['GET', 'POST'])
@login_required
def new_data():
    form = NewDataForm()
    if form.validate_on_submit():
        collections = Collection(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(collections)
        db.session.commit()

        flash('Add data', 'success')
        return redirect(url_for('main.home'))


    return render_template('create_data.html', title="New data", form=form, legend="New data")


@datas.route("/data/<data_id>")
def data(data_id):
    data = Collection.query.get_or_404(data_id)
    return render_template('data.html', title=data.title, data=data)


@datas.route("/data/<data_id>/update", methods=['GET', 'POST'])
@login_required
def updatedata(data_id):
    data = Collection.query.get_or_404(data_id)
    if(data.author != current_user):
        abort(403)
    form = NewDataForm()
    if form.validate_on_submit():
        data.title = form.title.data
        data.content = form.content.data
        db.session.commit()
        flash('Data updated!', 'success')
        return redirect(url_for('datas.data', data_id=data.id))

    elif request.method == 'GET':

        form.title.data =  data.title
        form.content.data = data.content
    return render_template('create_data.html', title="Update data", form=form, legend="Update data")


@datas.route("/data/<data_id>/delete", methods=['GET', 'POST'])
@login_required
def deletedata(data_id):
    data = Collection.query.get_or_404(data_id)
    if(data.author != current_user):
        abort(403)
    db.session.delete(data)
    db.session.commit()
    flash('Data has been deleted!', 'success')
    return redirect(url_for('.main.home'))

