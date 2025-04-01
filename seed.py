from app import db, Hero, Power, HeroPower, Episode, Guest, Appearance, app

# Create sample data
def seed_data():
    # Create heroes
    hero1 = Hero(name="Kamala Khan", super_name="Ms. Marvel")
    hero2 = Hero(name="Doreen Green", super_name="Squirrel Girl")
    
    # Create powers
    power1 = Power(name="super strength", description="gives the wielder super-human strengths")
    power2 = Power(name="flight", description="gives the wielder the ability to fly through the skies at supersonic speed")

    # Create episodes
    episode1 = Episode(date="1/11/99", number=1)
    episode2 = Episode(date="1/12/99", number=2)

    # Create guests
    guest1 = Guest(name="Michael J. Fox", occupation="actor")
    guest2 = Guest(name="Sandra Bernhard", occupation="Comedian")

    # Create appearances
    appearance1 = Appearance(rating=4, episode=episode1, guest=guest1)
    appearance2 = Appearance(rating=5, episode=episode2, guest=guest2)

    # Add to session and commit
    db.session.add_all([hero1, hero2, power1, power2, episode1, episode2, guest1, guest2, appearance1, appearance2])
    db.session.commit()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create tables
        seed_data()      # Seed the database
