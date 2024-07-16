from flask import Flask, request, send_file, jsonify, render_template, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from PIL import Image
import io
import zipfile

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# User class and in-memory user store for simplicity
class User(UserMixin):
    users = {}

    def __init__(self, id, username, password_hash, email=None):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.email = email  # Add email attribute

    @classmethod
    def get(cls, username):
        for user in cls.users.values():
            if user.username == username:
                return user
        return None

    @classmethod
    def add(cls, user):
        cls.users[user.id] = user

@login_manager.user_loader
def load_user(user_id):
    return User.users.get(user_id)

# Route for user signup
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']  # Collect email
        if User.get(username):
            flash('Username already exists', 'danger')
        else:
            user_id = str(len(User.users) + 1)
            password_hash = generate_password_hash(password)
            user = User(user_id, username, password_hash, email)
            User.add(user)
            flash('Signup successful. Please login.', 'success')
            return redirect(url_for('login'))
    return render_template('signup.html')

# Route for user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.get(username)
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash('Logged in successfully.', 'success')
            return redirect(url_for('index'))
        flash('Invalid username or password', 'danger')
    return render_template('login.html')

# Route for user logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

# Route for the home page
@app.route('/')
@login_required
def index():
    return render_template('index.html')

# Profile route
@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

# Route for image compression
@app.route('/compress', methods=['POST'])
def compress_image():
    if 'files' not in request.files:
        return jsonify({'error': 'No files provided'}), 400
    
    files = request.files.getlist('files')
    quality = int(request.form.get('quality', 70))
    compressed_files = []

    for file in files:
        image = Image.open(file)
        output_io = io.BytesIO()
        image.save(output_io, 'JPEG', quality=quality)
        output_io.seek(0)
        compressed_files.append(output_io)

    # Zip files for download
    zip_io = io.BytesIO()
    with zipfile.ZipFile(zip_io, 'w') as zip_file:
        for idx, file in enumerate(compressed_files):
            zip_file.writestr(f"compressed_{idx}.jpg", file.read())
    zip_io.seek(0)
    
    return send_file(zip_io, mimetype='application/zip', as_attachment=True, download_name='compressed_images.zip')

if __name__ == '__main__':
    app.run(debug=True)

