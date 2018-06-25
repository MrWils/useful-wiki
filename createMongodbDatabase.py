

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

# Function to insert new wiki
def InsertNewWiki(icon, name, description, link, tags):
    wiki_collection.insert_one({
        "icon": icon,
        "name": name,
        "description": description,
        "link": link,
        "tags": tags
    })

# CREATE DOCUMENTS
InsertNewWiki('none', 'Wikipedia', '/', 'www.wikipedia.com', ['general'])
InsertNewWiki('none', 'Encyclopedia dramatica', '/', 'www.encyclopediadramatica.rs', ['NSFW'])
InsertNewWiki('none', 'PRISM-break', '/', 'www.prism-break.org', ['privacy'])

# PRINT COMPLETE
print('Database created succesfully!')
