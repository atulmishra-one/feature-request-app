from flask import Blueprint
from flask import render_template

app_views = Blueprint('views', __name__, url_prefix='/')


@app_views.route('')
def index():
    return render_template("index.html")
