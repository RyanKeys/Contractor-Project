from flask import Flask, render_template, url_for, request, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient()
db = client.Website
guitars = db.guitars


app = Flask(__name__)

'''guitars = [
    {'name': 'Gibson', "type": "Les Paul"},
    {'name': 'Fender', "type": "Strat"}
]'''


@app.route('/')
def guitars_index():
    return render_template('guitars_index.html', guitars=guitars.find())


@app.route('/guitars', methods=['POST'])
def submit_listing():
    guitar = {
        'name': request.form.get('name'),
        'description': request.form.get('description')
    }
    guitar_id = guitars.insert_one(guitar).inserted_id
    return redirect(url_for('guitars_show', guitar_id=guitar_id))


@app.route('/guitars/new')
def guitars_new():
    return render_template("guitars_new.html")


@app.route('/guitars/<guitar_id>')
def guitars_show(guitar_id):
    guitar = guitars.find_one({'_id': ObjectId(guitar_id)})
    return render_template("guitars_show.html", guitar=guitar)


@app.route('/guitars/<guitar_id>/edit')
def guitars_edit(guitar_id):
    """Show the edit form for a guitar."""
    guitar = guitars.find_one({'_id': ObjectId(guitar_id)})
    return render_template('guitars_edit.html', guitar=guitar)


@app.route('/guitars/<guitar_id>', methods=['POST'])
def guitars_update(guitar_id):
    """Submit an edited guitar."""
    updated_guitar = {
        'name': request.form.get('name'),
        'description': request.form.get('description'),
    }
    guitars.update_one(
        {'_id': ObjectId(guitar_id)},
        {'$set': updated_guitar})
    return redirect(url_for('guitars_show', guitar_id=guitar_id))


@app.route('/guitars/<guitar_id>/delete', methods=['POST'])
def guitars_delete(guitar_id):
    """Delete one guitar."""
    guitars.delete_one({'_id': ObjectId(guitar_id)})
    return redirect(url_for('guitars_index'))
