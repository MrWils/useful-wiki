

# This website is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This website is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this website.  If not, see <https://www.gnu.org/licenses/>.


# IMPORTS
from flask_table import Table, Col
from flask import Flask, request, url_for, render_template
from pymongo import MongoClient
from constant import Constant
from pprint import pprint

# RUN-SETTINGS
app = Flask(__name__)

# DATABASE
# Connect with MongoLocalServer
client = MongoClient(Constant.MONGODB_HOST_LOCATION, Constant.MONGODB_PORT)

# Make database useful-wiki if not exists
db = client.useful_wiki

# Make our collections if not exists
wiki_collection = db['wiki_collection']

# ROUTES
@app.route('/')
def home():
    sort     = request.args.get('sort', 'name')
    reverse  = (request.args.get('direction', 'asc') == 'desc')
    tags     = request.args.getlist('tags')

    wikiTable = SortableTable(
        Item.get_sorted_by(sort, reverse),
            sort_by      = sort,
            sort_reverse = reverse
    )

    return render_template(
        'index.html',
        wikiTable = wikiTable,
        tags      = tags
    )

@app.route('/about/')
def about():
    return render_template(
        'html/about.html'
    )

@app.route('/addWiki/')
def addWiki():
    return render_template(
        'html/addWiki.html'
    )

@app.route('/requestTag/')
def requestTag():
    return render_template(
        'html/requestTag.html'
    )

@app.route('/contact/')
def contact():
    return render_template(
        'html/contact.html'
    )

@app.route('/donate/')
def donate():
    return render_template(
        'html/donate.html'
    )

# WIKI-TABLE
# TODO: Add icon support
# TODO: Make the wiki-links clickable
# TODO: Make a working searchbox
class SortableTable(Table):
    icon        = Col('Icon', allow_sort = False)
    name        = Col('Name')
    description = Col('Description')
    link        = Col('Link', allow_sort = False)
    allow_sort  = True

    def sort_url(self, col_key, reverse = False):
        tags = request.args.getlist('tags')

        if reverse:
            direction = 'desc'
        else:
            direction = 'asc'

        return url_for('home',
            sort      = col_key,
            direction = direction,
            tags      = tags
        )

# DATABASE ITEMS
class Item(object):
    def __init__(self, icon, name, description, link, tags=[]):
        self.icon        = icon
        self.name        = name
        self.description = description
        self.link        = link
        self.tags        = tags

    @classmethod
    def get_sorted_by(cli, sort, reverse=False):
        tags = request.args.getlist('tags')
        data = Item.get_elements()

        for item in data:
            if 'NSFW' in item.tags and 'NSFW' not in tags:
                data.remove(item)

        return sorted(
           data,
           key     = lambda x: getattr(x, sort),
           reverse = reverse
        )

    @classmethod
    def get_elements(cli):
        try:
            wikis = []
            wiki_documents = wiki_collection.find({})

            for wiki in wiki_documents:
                wikis.append(Item(wiki['icon'], wiki['name'], wiki['description'], wiki['link'], wiki['tags']))

            return wikis

        except Exception:
            return ['none', 'Error', 'Error, while reading the database', 'www.useful-wiki.com', ['Error']]

# RUN THE APP
if __name__ == '__main__':
    app.run(host=Constant.WEBHOST_LOCATION, port=Constant.WEBHOST_PORT)
