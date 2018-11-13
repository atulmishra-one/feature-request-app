""""App views
This views serves all the static pages of the feature app

"""

from flask import Blueprint
from flask import render_template

app_views = Blueprint('views', __name__, url_prefix='/')


@app_views.route('')
def index():
    return render_template("index.html")


@app_views.route('/request_feature')
def request_feature():
    return render_template("create_feature.html")

