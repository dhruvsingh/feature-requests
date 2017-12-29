from fr_app import app
from flask import render_template, redirect, url_for
from .models import db, FeatureRequest
from .forms import FeatureRequestForm


@app.route('/')
def home_page():
    features = FeatureRequest.query.all()
    return render_template(
        'index.html',
        title='All Requests',
        home_active='active',
        features=features
    )


@app.route('/feature/add/', methods=('GET', 'POST'))
@app.route('/feature/<int:id>/', methods=('GET', 'POST'))
def add_update_feature(id=None):
    """Add/update a feature request."""
    if id:
        fr = FeatureRequest.query.filter_by(id=id).first() or FeatureRequest()
        form = FeatureRequestForm(obj=fr)
        title = "Editing '{}'".format(fr.title)
        action = 'edit'
    else:
        fr = FeatureRequest()
        form = FeatureRequestForm()
        title = 'Creating a New Feature Request'
        action = 'add'

    if form.validate_on_submit():
        form.populate_obj(fr)
        db.session.add(fr)
        db.session.commit()

        return redirect(url_for('home_page'))

    return render_template(
        'add_update_feature_request.html',
        form=form,
        title=title,
        action=action,
        feature_active='active'
    )
