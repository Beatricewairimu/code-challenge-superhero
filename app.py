from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///heroes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Hero(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    super_name = db.Column(db.String, nullable=False)
    hero_powers = db.relationship('HeroPower', backref='hero', cascade='all, delete-orphan')

class Power(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    hero_powers = db.relationship('HeroPower', backref='power', cascade='all, delete-orphan')

class HeroPower(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String, nullable=False)
    hero_id = db.Column(db.Integer, db.ForeignKey('hero.id'), nullable=False)
    power_id = db.Column(db.Integer, db.ForeignKey('power.id'), nullable=False)

    @db.validates('strength')
    def validate_strength(self, key, strength):
        if strength not in ['Strong', 'Weak', 'Average']:
            raise ValueError("Strength must be one of the following values: 'Strong', 'Weak', 'Average'.")
        return strength

    @db.validates('power_id')
    def validate_power(self, key, power_id):
        if not Power.query.get(power_id):
            raise ValueError("Power does not exist.")
        return power_id

    @db.validates('hero_id')
    def validate_hero(self, key, hero_id):
        if not Hero.query.get(hero_id):
            raise ValueError("Hero does not exist.")
        return hero_id

class Episode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String, nullable=False)
    number = db.Column(db.Integer, nullable=False)
    appearances = db.relationship('Appearance', backref='episode', cascade='all, delete-orphan')

class Guest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    occupation = db.Column(db.String, nullable=False)
    appearances = db.relationship('Appearance', backref='guest', cascade='all, delete-orphan')

class Appearance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    episode_id = db.Column(db.Integer, db.ForeignKey('episode.id'), nullable=False)
    guest_id = db.Column(db.Integer, db.ForeignKey('guest.id'), nullable=False)

    @db.validates('rating')
    def validate_rating(self, key, rating):
        if rating < 1 or rating > 5:
            raise ValueError("Rating must be between 1 and 5.")
        return rating

@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    return [{'id': hero.id, 'name': hero.name, 'super_name': hero.super_name} for hero in heroes]

@app.route('/heroes/<int:id>', methods=['GET'])
def get_hero(id):
    hero = Hero.query.get(id)
    if hero:
        return {
            'id': hero.id,
            'name': hero.name,
            'super_name': hero.super_name,
            'hero_powers': [{'hero_id': hp.hero_id, 'id': hp.id, 'power': {'description': hp.power.description, 'id': hp.power.id, 'name': hp.power.name}, 'power_id': hp.power_id, 'strength': hp.strength} for hp in hero.hero_powers]
        }
    return {'error': 'Hero not found'}, 404

@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    return [{'id': power.id, 'name': power.name, 'description': power.description} for power in powers]

@app.route('/powers/<int:id>', methods=['GET'])
def get_power(id):
    power = Power.query.get(id)
    if power:
        return {'id': power.id, 'name': power.name, 'description': power.description}
    return {'error': 'Power not found'}, 404

@app.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    power = Power.query.get(id)
    if not power:
        return {'error': 'Power not found'}, 404

    data = request.get_json()
    if 'description' in data:
        if len(data['description']) < 20:
            return {'errors': ['Description must be at least 20 characters long.']}, 400
        power.description = data['description']
    
    db.session.commit()
    return {'id': power.id, 'name': power.name, 'description': power.description}

@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.get_json()
    try:
        new_hero_power = HeroPower(strength=data['strength'], hero_id=data['hero_id'], power_id=data['power_id'])
        db.session.add(new_hero_power)
        db.session.commit()
        return {
            'id': new_hero_power.id,
            'hero_id': new_hero_power.hero_id,
            'power_id': new_hero_power.power_id,
            'strength': new_hero_power.strength,
            'hero': {'id': new_hero_power.hero.id, 'name': new_hero_power.hero.name, 'super_name': new_hero_power.hero.super_name},
            'power': {'id': new_hero_power.power.id, 'name': new_hero_power.power.name, 'description': new_hero_power.power.description}
        }, 201
    except ValueError as e:
        return {'errors': [str(e)]}, 400

@app.route('/episodes', methods=['GET'])
def get_episodes():
    episodes = Episode.query.all()
    return [{'id': episode.id, 'date': episode.date, 'number': episode.number} for episode in episodes]

@app.route('/episodes/<int:id>', methods=['GET'])
def get_episode(id):
    episode = Episode.query.get(id)
    if episode:
        return {
            'id': episode.id,
            'date': episode.date,
            'number': episode.number,
            'appearances': [{'id': appearance.id, 'rating': appearance.rating, 'guest_id': appearance.guest_id, 'guest': {'id': appearance.guest.id, 'name': appearance.guest.name, 'occupation': appearance.guest.occupation}} for appearance in episode.appearances]
        }
    return {'error': 'Episode not found'}, 404

@app.route('/guests', methods=['GET'])
def get_guests():
    guests = Guest.query.all()
    return [{'id': guest.id, 'name': guest.name, 'occupation': guest.occupation} for guest in guests]

@app.route('/appearances', methods=['POST'])
def create_appearance():
    data = request.get_json()
    try:
        new_appearance = Appearance(rating=data['rating'], episode_id=data['episode_id'], guest_id=data['guest_id'])
        db.session.add(new_appearance)
        db.session.commit()
        return {
            'id': new_appearance.id,
            'rating': new_appearance.rating,
            'guest_id': new_appearance.guest_id,
            'episode_id': new_appearance.episode_id,
            'episode': {'id': new_appearance.episode.id, 'date': new_appearance.episode.date, 'number': new_appearance.episode.number},
            'guest': {'id': new_appearance.guest.id, 'name': new_appearance.guest.name, 'occupation': new_appearance.guest.occupation}
        }, 201
    except ValueError as e:
        return {'errors': [str(e)]}, 400

if __name__ == '__main__':
    app.run(debug=True)
