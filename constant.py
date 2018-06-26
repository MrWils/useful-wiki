

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


class Constant():

    # CONFIGURATION

    # MONGODB
    # MONGO_HOST_LOCATION
    MONGODB_HOST_LOCATION = 'localhost'
    # MONGODB PORT
    MONGODB_PORT = 12345
    # default port (not working for me for some reason)
    # default: 27017

    # WEBHOST
    # HOST_LOCATION
    WEBHOST_LOCATION = '0.0.0.0'
    # PORT
    WEBHOST_PORT = '80'

    # MAIL SETTINGS
    MAIL_SERVER   = 'smtp.gmail.com'
    MAIL_PORT     = 465
    MAIL_USERNAME = 'me@gmail.com'
    MAIL_PASSWORD = '''******'''
    MAIL_USE_TLS  = False
    MAIL_USE_SSL  = True
    # You may have to decrease the security level.
    # Please log in to your Gmail account and visit this link to decrease the security.
    # https://myaccount.google.com/intro/security

    # VALIDATOR SETTINGS
    MIN_WIKI_NAME_LENGTH = 10
    MAX_WIKI_NAME_LENGTH = 25

    MIN_WIKI_DESCRIPTION_LENGTH = 100
    MAX_WIKI_DESCRIPTION_LENGTH = 250

    MIN_TAG_NAME_LENGTH = 4
    MAX_TAG_NAME_LENGTH = 25

    MIN_TAG_DESCRIPTION_LENGTH = 35
    MAX_TAG_DESCRIPTION_LENGTH = 250
