from flask import Flask, render_template, flash, redirect, url_for
from forms import  RegistrationForm, LoginForm

app = Flask(__name__)

app.config['SECRET_KEY']= '4af1676bcc923bbdd62b174e858f53e7'

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

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account create form {form.username.data}!', 'success')
        return redirect(url_for('home'))

    return render_template('register.html', title="Register", form=form)

@app.route("/login")
def login():
    form = LoginForm()
    return render_template('login.html', title="Register", form=form)



if __name__ == '__main__':
   app.run(debug=True)