import json
from flask import request, render_template, Blueprint
from models.item import Item

item_blueprint = Blueprint('items', __name__)


@item_blueprint.route('/')
def index():
    items = Item.all()
    return render_template('items/index.html', items=items)


@item_blueprint.route('/new', methods=['GET', 'POST'])
def new_item():
    if request.method == 'POST':
        query = json.loads(request.form['query'])
        Item(request.form['url'], request.form['tag_name'], query).save_to_mongo()

    return render_template('items/new_item.html')