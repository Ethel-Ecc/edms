import os
import secrets

from flask import Blueprint, flash, redirect, url_for, render_template, abort, request
from flask_login import login_required, current_user

from edms import db
from edms.datasets.forms import AddDatasetForm
from edms.models import Dataset

datasets = Blueprint('datasets', __name__)


# This method handles the dataset option
def save_dataset(form_dataset):
    random_hex = secrets.token_hex(8)
    _, dataset_ext = os.path.splitext(form_dataset.filename)
    dataset_filename = random_hex + dataset_ext
    dataset_path = os.path.join(app.root_path, 'static/datasets', dataset_filename)
    form_dataset.save(dataset_path)

    return dataset_filename


# This handles add dataset routes
@datasets.route('/dataset/add', methods=['GET', 'POST'])
@login_required
def add_dataset():
    form = AddDatasetForm()
    if form.validate_on_submit():
        dataset_new = Dataset(
            name_or_title=form.name_or_title.data,
            distribution_license=form.distribution_license.data,
            format=form.format.data,
            description=form.description.data,
            download_url=form.download_url.data,
            owner=current_user
        )
        db.session.add(dataset_new)
        db.session.commit()

        flash('Dataset added successfully', 'success')

        return redirect(url_for('main.homepage'))

    return render_template('pages/add_dataset.html',
                           title='Add Dataset',
                           form=form,
                           legend='Add new dataset')


# This handles each dataset via its id
@datasets.route('/dataset/details/<int:dataset_id>')
def dataset_details(dataset_id):
    dataset = Dataset.query.get_or_404(dataset_id)
    return render_template('pages/dataset.html', title=dataset.name_or_title, dataset=dataset)


# This handles each dataset via its id for updating.
@datasets.route('/dataset/details/<int:dataset_id>/update', methods=['GET', 'POST'])
@login_required
def dataset_update(dataset_id):
    dataset = Dataset.query.get_or_404(dataset_id)
    if dataset.owner != current_user:
        abort(403)
    form = AddDatasetForm()

    if form.validate_on_submit():
        dataset.name_or_title = form.name_or_title.data
        dataset.distribution_license = form.distribution_license.data
        dataset.format = form.format.data
        dataset.description = form.description.data
        dataset.download_url = form.download_url.data

        db.session.commit()

        flash('dataset successfully updated', 'success')
        return redirect(url_for('datasets.dataset_details', dataset_id=dataset_id))

    elif request.method == 'GET':
        form.name_or_title.data = dataset.name_or_title,
        form.distribution_license.data = dataset.distribution_license,
        form.format.data = dataset.format,
        form.description.data = dataset.description
        form.download_url.data = dataset.download_url

    return render_template('pages/add_dataset.html',
                           title='Update Dataset',
                           form=form,
                           legend='Update Dataset'
                           )


@datasets.route('/dataset/<int:dataset_id>/delete', methods=['POST'])
@login_required
def delete_dataset(dataset_id):
    dataset = Dataset.query.get_or_404(dataset_id)
    if dataset.owner != current_user:
        abort(403)

    db.session.delete(dataset)
    db.session.commit()
    flash('The dataset has been deleted successfully', 'success')
    return redirect(url_for('main.homepage'))
