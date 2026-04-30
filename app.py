from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User
from forms import LoginForm, RegisterForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pet_adoption.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

from models import User, Pet
from forms import LoginForm, RegisterForm

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.before_first_request
def create_tables():
    with app.app_context():
        db.create_all()
        if not Pet.query.first():
            correct_data = {
                1: ("Buster", "Brown Pitbull Mix", "2 Years"),
                2: ("Charlie", "Shih Tzu Mix", "4 Years"),
                3: ("Whiskers", "Graphic Art Cat", "Unknown"),
                4: ("Thumper", "Brown & White Rabbit", "1 Year"),
                5: ("Max", "Tan Terrier Mix", "3 Years"),
                6: ("Oreo", "Black & White Rabbit", "6 Months"),
                7: ("Bandit", "Cattle Dog Mix", "1.5 Years"),
                8: ("Luna", "Grey & White Cat", "2 Years"),
                9: ("Garfield", "Orange Fluffy Cat", "3 Years"),
                10: ("Simba", "Tabby Kitten", "3 Months"),
                11: ("Bella", "White & Brown Cat", "4 Years"),
                12: ("Snowball", "Cream Kitten", "2 Months"),
                13: ("Buddy & Chloe", "Dog & Cat Bonded Pair", "2 Years"),
                14: ("Peanut & Butter", "Guinea Pigs", "1 Year"),
                15: ("Shadow", "Black Lab Mix Puppy", "4 Months")
            }
            pets_data = [
                {"name": correct_data[i][0], "breed": correct_data[i][1], "age": correct_data[i][2], "image_url": f"images/image{i}.jpg"}
                for i in range(1, 16)
            ]
            for p_data in pets_data:
                pet = Pet(**p_data)
                db.session.add(pet)
            db.session.commit()
            print("Database seeded with pets.")

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    print(f"Request method: {request.method}")
    print(f"Form data: {request.form}")

    if form.validate_on_submit():
        print("Form validation passed!")
        user = User.query.filter_by(email=form.email.data).first()
        print(f"User found: {user}") 
        
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Login successful')
            return redirect(url_for('index'))
        else:
            print("Invalid credentials!")
            flash('Invalid email or password')

    else:
        print("Form validation failed!")
        print(form.errors)  

    return render_template('login.html', form=form)



@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegisterForm()
    print(f"Request method: {request.method}")
    print(f"Form data: {request.form}")

    if form.validate_on_submit():
        print("Form validation passed!")
        
    
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            print("User already exists!")
            flash("Email is already registered. Please log in.")
            return redirect(url_for('login'))

        hashed_password = generate_password_hash(form.password.data)
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password
        )

        try:
            db.session.add(user)
            db.session.commit()
            flash('Registration successful! Please log in.')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            print(f"Error during registration: {e}")
            flash('An error occurred. Please try again.')

    else:
        print("Form validation failed!")
        print(form.errors) 

    return render_template('register.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('home'))

@app.route('/index')
def index():
    pets = Pet.query.all()
    return render_template('index.html', pets=pets)

@app.route('/adopt/<int:pet_id>', methods=['POST'])
@login_required
def adopt(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    if not pet.is_adopted:
        pet.is_adopted = True
        pet.owner_id = current_user.id
        db.session.commit()
        flash(f'You have successfully adopted {pet.name}!', 'success')
    else:
        flash(f'Sorry, {pet.name} is already adopted.', 'error')
    return redirect(url_for('index'))

@app.route('/my_pets')
@login_required
def my_pets():
    user_pets = Pet.query.filter_by(owner_id=current_user.id).all()
    return render_template('my_pets.html', pets=user_pets)

if __name__ == "__main__":
    app.run(debug=True)