

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
from flask import Flask, request, url_for, render_template

from flask_table import Table, Col
from flask_mail import Mail, Message

from pymongo import MongoClient
from constant import Constant

# RUN-SETTINGS
app = Flask(__name__)

# IMPORT MAIL SETTINGS
app.config['MAIL_SERVER']   = Constant.MAIL_SERVER
app.config['MAIL_PORT']     = Constant.MAIL_PORT
app.config['MAIL_USERNAME'] = Constant.MAIL_USERNAME
app.config['MAIL_PASSWORD'] = Constant.MAIL_PASSWORD
app.config['MAIL_USE_TLS']  = Constant.MAIL_USE_TLS
app.config['MAIL_USE_SSL']  = Constant.MAIL_USE_SSL

mail = Mail(app)

# golbal validators
wiki_validator = {
    "wikiNameValidator":        "valid",
    "wikiDescriptionValidator": "valid",
    "wikiURLValidator":         "valid",
    "wikiTagsValidator":        "valid"
}
tag_validator = {
    "tagNameLengthValidator":  "valid",
    "tagNameSpacesValidator":  "valid",
    "tagDescriptionValidator": "valid"
}

@app.route('/requestWiki/sendMail/')
def sendWikiMail():
    validator = wiki_validator

    # Get values
    wikiName        = request.args.get('wikiName')
    wikiDescription = request.args.get('wikiDescription')
    wikiURL         = request.args.get('wikiURL')
    wikiTags        = request.args.get('wikiTags').strip().split(',')

    # Validate
    # TODO: Fix validator problems
    # TODO: Add wikiName has to be unique validation
    if len(wikiName) < Constant.MIN_WIKI_NAME_LENGTH:
        validator["wikiNameValidator"] = "The minimum name length is " + str(Constant.MIN_WIKI_NAME_LENGTH)
    elif len(wikiName) > Constant.MAX_WIKI_NAME_LENGTH:
        validator["wikiNameValidator"] = "The maximum name length is " + str(Constant.MAX_WIKI_NAME_LENGTH)

    if len(wikiDescription) < Constant.MIN_WIKI_DESCRIPTION_LENGTH:
        validator["wikiDescriptionValidator"] = "The minimum description length is " + str(Constant.MIN_WIKI_DESCRIPTION_LENGTH)
    elif len(wikiDescription) > Constant.MAX_WIKI_DESCRIPTION_LENGTH:
        validator["wikiDescriptionValidator"] = "The maximum description length is " + str(Constant.MAX_WIKI_DESCRIPTION_LENGTH)

    if 'www.' not in wikiURL or wikiURL.count(".") < 2:
        validator["wikiURLValidator"] = "Please use a valid URL like 'www.my-useful-wiki.com'"

    valid_tags = True
    invalid_tags = ""
    for tag in wikiTags:
        if tag not in tag_collection.find({}):
            valid_tags = False
            invalid_tags += tag + ' '

    if valid_tags == False:
        validator["wikiTagsValidator"] = "Some of your tags are invalid: " + invalid_tags

    isEverythingValid = True
    for validation in validator:
        if validation != 'valid':
            isEverythingValid=False

    if isEverythingValid:
        print("mail sent")
        msg = Message('Wiki_Request', sender = 'useful-wiki',
            recipients = [MAIL_USERNAME])

        msg.body = mailBody
        mail.send(msg)

    return render_template(
        'html/requestWiki.html',
        MailIsSent = isEverythingValid,
        validator  = validator
    )

@app.route('/requestTag/sendMail/')
def sendTagMail():
        validator = tag_validator

        # Get values
        tagName  = request.args.get('tagName')
        tagDescription = request.args.get('tagDescription')

        # Validate
        # TODO: Add tagName has to be unique validation
        if " " in tagName:
            validator["tagNameSpacesValidator"] = "A tag can't contain spaces"
        if len(tagName) < Constant.MIN_TAG_NAME_LENGTH:
            validator["tagNameLengthValidator"] = "The minimum tag length is " + str(Constant.MIN_TAG_NAME_LENGTH)
        elif len(tagName) > Constant.MAX_TAG_NAME_LENGTH:
            validator["tagNameLengthValidator"] = "The maximum tag length is " + str(Constant.MAX_TAG_NAME_LENGTH)

        if len(tagDescription) < Constant.MIN_TAG_DESCRIPTION_LENGTH:
            validator["tagDescriptionValidator"] = "The minimum description length is " + str(Constant.MIN_TAG_DESCRIPTION_LENGTH)
        elif len(tagDescription) > Constant.MAX_TAG_DESCRIPTION_LENGTH:
            validator["tagDescriptionValidator"] = "The maximum description length is " + str(Constant.MAX_TAG_DESCRIPTION_LENGTH)

        isEverythingValid = True
        for validation in validator:
            if validation != 'valid':
                isEverythingValid = False

        if isEverythingValid:
            msg = Message('Tag_Request', sender = 'useful-wiki',
                recipients = [MAIL_USERNAME])

            msg.body = '<h1>' + tagName + '</h1><p>' + tagDescription + '</p>'
            mail.send(msg)

        return render_template(
            'html/requestTag.html',
            MailIsSent = isEverythingValid,
            validator  = validator
        )

# DATABASE
# Connect with MongoLocalServer
client = MongoClient(Constant.MONGODB_HOST_LOCATION, Constant.MONGODB_PORT)

# Make database useful-wiki if not exists
db = client.useful_wiki

# Make our collections if not exists
wiki_collection = db['wiki_collection']
tag_collection  = db['tag_collection']

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

@app.route('/requestWiki/')
def requestWiki():
    return render_template(
        'html/requestWiki.html',
        validator = wiki_validator
    )

@app.route('/requestTag/')
def requestTag():
    return render_template(
        'html/requestTag.html',
        validator = tag_validator
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
    def __init__(self, icon, name, description, link, tags = []):
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
        wikis = []

        try:
            wiki_documents = wiki_collection.find({})

            for wiki in wiki_documents:
                wikiTags = []

                for tagId in wiki['tagIds']:
                    tagName = tag_collection.find_one(
                        {"_id": tagId}
                    ).get('name')
                    print(tagName)

                    if tagName is not None:
                        wikiTags.append(tagName)
                    else:
                        return [Item(
                            'none', 'Error', 'Error, invalid tag in tags',
                            'www.useful-wiki.com', ['Error'])]

                wikis.append(
                    Item(
                        wiki['icon'], wiki['name'],
                        wiki['description'], wiki['link'], wikiTags
                    )
                )

            if wikis is None or len(wikis) == 0:
                return [Item(
                    'none', 'Error', 'Error, couldn\'t find any wikis',
                    'www.useful-wiki.com', ['Error'])]

            return wikis

        except Exception:
            return [Item(
                'none', 'Error', 'Unknown error, while reading the database',
                'www.useful-wiki.com', ['Error'])]

# RUN THE APP
if __name__ == '__main__':
    app.run(host = Constant.WEBHOST_LOCATION, port = Constant.WEBHOST_PORT)
