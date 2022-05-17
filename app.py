from flask import Flask, render_template
app = Flask(__name__)

# App Routes
@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/signup')
def sign_up():
    return render_template('signup.html')

@app.route('/profile/<user>')
def user_profile(user):
    return render_template('user-profile.html', name=user)



if __name__ == '__main__':
    app.debug = True
    app.run(debug = True)