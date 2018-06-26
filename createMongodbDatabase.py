

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
from pymongo import MongoClient
from constant import Constant

# CREATE DATABASE
# Connect with MongoLocalServer
client = MongoClient(Constant.MONGODB_HOST_LOCATION, Constant.MONGODB_PORT)

# Recreate database useful-wiki
client.drop_database('useful_wiki')
db = client.useful_wiki

# Make our collections
wiki_collection = db['wiki_collection']
tag_collection  = db['tag_collection']

# FUNCTIONS
# Function to insert new wiki
# Returns None on error
def InsertNewWiki(icon, name, description, link, tags):
    tagIds = []

    try:
        for tag in tags:
            tagId = GetTagId(tag)

            if tagId is None:
                tagId = InsertTag(tag)

            tagIds.append(tagId)

        wiki_collection.insert_one({
            "icon":        icon,
            "name":        name,
            "description": description,
            "link":        link,
            "tagIds":      tagIds
        })

    except Exception:
        return None

# Function to insert a new tag,
# The method will return 'None' when an error appears
def InsertTag(tagName):
    try:
        return tag_collection.insert_one({
            "name": tagName
        }).inserted_id

    except Exception:
        return None

    return tagId

# Function will get the TagId,
# The method will return 'None' when an error appears
def GetTagId(tagName):
    try:
        return tag_collection.find_one({"name": tagName}).get('_id')

    except Exception:
        return None

# CREATE DOCUMENTS
InsertNewWiki('none', 'Wikipedia', 'Wikipedia is a free online encyclopedia, created and edited by volunteers around the world and hosted by the Wikimedia Foundation.', 'www.wikipedia.com', ['general'])
InsertNewWiki('none', 'Encyclopedia dramatica', 'Encyclopedia Dramatica is a satirical website, consisting of a wiki that uses MediaWiki software.', 'www.encyclopediadramatica.rs', ['NSFW'])
InsertNewWiki('none', 'PRISM-break', 'Get rid of worldwide bugging and spying programs like PRISM, XKeyscore and Tempora. Stop government data monitoring programs by encrypting your communication and putting an end to your dependence on proprietary services.', 'www.prism-break.org', ['privacy'])

# PRINT COMPLETE
print('Database created succesfully!')
