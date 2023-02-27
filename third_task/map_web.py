"""
Map web app
"""
import os
from flask import Flask, render_template, request
from map_song import main_function

app = Flask(__name__)

@app.route('/map', methods=['POST'])
def do_search():
    """
    Searches for the best song of an artist and creates a  map
    """
    phrase = request.form['phrase']
    main_function(phrase)
    return render_template('songs_map.html')

@app.route('/')
@app.route('/entry')
def entry_page():
    """
    Creates an entry page
    """
    return render_template('base.html', the_title='Map generator')

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    app.run(debug = True)
