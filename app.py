from flask import Flask, render_template


app = Flask(__name__)

posts = [{
    'title': 'test',
    'description': 'simple descfsdfs'

},
{
    'title': 'test',
    'description': 'simple descfsdfs'

},
{
    'title': 'test',
    'description': 'simple descfsdfs'

}

]
@app.route("/")
def hello_world():
    return  render_template('home.html', posts=posts)

@app.route("/about")
def about():
    return "<p>about</p>"



if __name__ == '__main__':
   app.run(debug=True)