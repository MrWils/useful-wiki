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
# from pymongo import MongoClient
# flash redirect request session abort

# RUN-SETTINGS
app = Flask(__name__)

# ROUTES
@app.route('/')
def home():
    sort      = request.args.get('sort', 'name')
    reverse   = (request.args.get('direction', 'asc') == 'desc')

    wikiTable = SortableTable(Item.get_sorted_by(sort, reverse),
        sort_by=sort,
        sort_reverse=reverse)

    return render_template(
        'index.html', wikiTable=wikiTable)

# @app.route('/<string:tags>/')
# def wikiSearch(tags):
#     return tags

@app.route('/about/')
def about():
    return render_template(
        'html/about.html')

@app.route('/addWiki/')
def addWiki():
    return render_template(
        'html/addWiki.html')

@app.route('/requestTag/')
def requestTag():
    return render_template(
        'html/requestTag.html')

@app.route('/contact/')
def contact():
    return render_template(
        'html/contact.html')

@app.route('/donate/')
def donate():
    return render_template(
        'html/donate.html')

# WIKI-TABLE
# TODO: Add icon support
# TODO: Make the wiki-link clickable
class SortableTable(Table):
    icon = Col('Icon', allow_sort=False)
    name = Col('Name')
    description = Col('Description')
    link = Col('Link', allow_sort=False)
    allow_sort = True

    def sort_url(self, col_key, reverse=False):
        if reverse:
            direction = 'desc'
        else:
            direction = 'asc'

        return url_for('home', sort=col_key, direction=direction)

# DEMO DATABASE
# TODO: Replace demo database with real mongodb database
class Item(object):
    def __init__(self, icon, name, description, link):
        self.icon = icon
        self.name = name
        self.description = description
        self.link = link

    @classmethod
    def get_elements(cls):
        return [
            Item('none', 'wikipedia', '/', 'www.wikipedia.com'),
            Item('none', 'encyclopedia dramatica', '/ {has NSFW tag}', 'www.encyclopediadramatica.rs'),
            Item('none', 'PRISM-break', '/', 'prism-break.org')]

    @classmethod
    def get_sorted_by(cls, sort, reverse=False):
        return sorted(
            cls.get_elements(),
            key=lambda x: getattr(x, sort),
            reverse=reverse)

# DATABASE
# from pymongo import MongoClient

# Connect with MongoLocalServer
# client = MongoClient('localhost', 27017)

# Make database useful-wiki if not exists
# db = client.useful_wiki

# Make our collections
# wiki_collection = db.pymongo_wikis

# Function to insert new wiki
#def insertNewWiki(icon, name, description, link, tags):
#    try:
#    wiki_collection.insert_one(
#        {"icon": icon,
#         "name": name,
#         "description": description,
#         "link": link,
#         "tags": tags,
#         })

# Function to update wiki
#def updateWiki(icon, name, description, link, tags):
#    try:
#    wiki_collection.update_one(
#        {"icon": icon,
#         "name": name,
#         "description": description,
#         "link": link,
#         "tags": tags,
#         })

# Function to get all wikis
#def getWikis():
#    try:
#    wikis=[]
#    wikiColumn = wiki_collection.find()

#    for wiki in wikiColumn:
#        wikis = wikis + wiki

#    return wikis

#    except Exception:
#        return ["error while reading wiki"]


# RUN THE APP
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)


