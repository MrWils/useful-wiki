#This website is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#This website is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this website.  If not, see <https://www.gnu.org/licenses/>.


from flask import Flask, flash, redirect, render_template, request, session, abort, json

app = Flask(__name__)

@app.route('/' or '/index.html/')
def home():
	return render_template(
		'index.html')

@app.route('/<string:tags>/' or '/index.html/<string:tags>/')
def wikiSearch(tags):
	return tags

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

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=80)

