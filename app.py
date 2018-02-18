from flask import Flask, render_template, request
from webbrowser import open_new_tab
import twitter_map

app = Flask(__name__)
name = ''
users = ''


@app.route("/", methods=['GET'])
def question():
    # First page where user will put information
    return render_template("hello.html")


@app.route("/maps", methods=['POST'])
def maps():
    global name, users
    # Takes information that user put
    name = request.form["log"]
    users = request.form["number"]
    # Look for location
    friends = twitter_map.search(name, users)
    # Search coordinates
    coordinates = twitter_map.do_coordinates(friends)
    # Create map
    twitter_map.do_map(coordinates)
    # Pahe with a map
    return render_template("Map_1.html")


if __name__ == "__main__":
    port = 5000
    open_new_tab('http://localhost:{0}'.format(port))
    app.run(port=port, debug=True)
