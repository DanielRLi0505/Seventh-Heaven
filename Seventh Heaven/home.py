from flask import Flask, redirect, render_template, send_from_directory, url_for
from flask_sqlalchemy import SQLAlchemy
import uuid

# make sure the script's directory is in Python's import path
# this is only required when run from a different directory
import os

from sqlalchemy import StaticPool, create_engine
# Determine the absolute path of our database file
scriptdir = os.path.abspath(os.path.dirname(__file__))

#TODO: choose database name
dbpath = os.path.join(scriptdir, 'database/seventh_heaven_sqlite.sqlite3')


# Complete app setup and config
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SECRET_KEY'] = 'winchocobobarretsword'
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{dbpath}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Getting the database object handle from the app
db = SQLAlchemy(app)
button_titles = ["Home", "Menu", "News", "Contact Us"]

class Dish(db.Model):
    __tablename__ = 'Dishes'
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.Unicode, nullable=False)
    description = db.Column(db.Unicode, nullable=False)
    cost = db.Column(db.Unicode, nullable=False)
    def __str__(self):
        return f"Dish(name={self.name}, description={self.description}, cost={self.cost})"
    def __repr__(self):
        return f"Dish({self.id})"
    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "cost": self.cost
        }
    
class Drink(db.Model):
    __tablename__ = 'Drinks'
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.Unicode, nullable=False)
    description = db.Column(db.Unicode, nullable=False)
    type = db.Column(db.Unicode, nullable=False)
    cost = db.Column(db.Unicode, nullable=False)
    def __str__(self):
        return f"Drink(name={self.name}, cost={self.cost})"
    def __repr__(self):
        return f"Drink({self.id})"
    def to_json(self):
        return {
            "drink_id": self.id,
            "drink_name": self.name,
            "drink_description": self.description,
            "drink_type": self.type,
            "drink_cost": self.cost
        }
    
class Article(db.Model):
    __tablename__ = 'Articles'
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    title = db.Column(db.Unicode, nullable=False)
    date = db.Column(db.Unicode, nullable=False)
    def __str__(self):
        return f"Article(title={self.title}, date={self.date})"
    def __repr__(self):
        return f"Article({self.id})"
    def to_json(self):
        return {
            "article_id": self.id,
            "article_title": self.title,
            "article_date": self.date,
        }

@app.before_request
def create_tables():
    """db.drop_all()
    db.create_all()
    db.session.add(Dish(name="Boneless Chocobo Wings", description="Our crispy wings come hand-breaded and rolled in your choice of sauce!  "
                        + "Available sauces include whiskey glaze, garlic parmesean, smokey BBQ, Asian zing, honey pepper, and Korean BBQ.",
                        cost=844))
    db.session.add(Dish(name="Mozzarella Sticks", description="This dish is nice and crunchy on the outside, soft and gooey on the inside, "
                        + "and delicious inside-out!  Served with marinara sauce.",
                        cost=195))
    db.session.add(Dish(name="Heaven's Burger", description="Our juicy signature burgers come with beef, lettuce, tomatoes, Worcestershire sauce, "
                        + "pepper jack cheese, bacon, and onions, all sandwiched between two buttery buns!",
                        cost=837))
    db.session.add(Dish(name="Potato Skins", description="Our crispy, golden brown potato skins are topped with cheddar cheese, bacon, and green onions!  " +
                        "Served with sour cream.",
                        cost=631))
    db.session.add(Dish(name="Loaded Fries", description="These crispy, golden brown fries are topped with cheddar cheese, bacon, and green onions!",
                        cost=811))
    db.session.add(Dish(name="French Onion Soup Bites", description="These are a nice spin on the classic French Onion Soup!  Bread crumbs, Gruyère cheese, onions, and beef broth, everything "
                        + "you love about the dish in a pastry!",
                        cost=231))
    db.session.add(Dish(name="Moogles Sleeping in Stars", description="Don't worry, we didn't use actual Moogle meat for this!  These are just "
                        + "little sausage bites rolled up in buttery, golden-brown, cheese-crusted croissant pieces and topped with more cheese.",
                        cost=891))
    db.session.add(Dish(name="Eggs and Chips", description="Your standard sunny-side-up eggs served with crispy, golden brown fries. "
                        + "These two things served together make quite a mouthwatering combination!",
                        cost=631))
    db.session.add(Dish(name="Pepperoni Pizza", description="Pepperoni and cheese with marinara sauce, all on a "
                        + "thin, crispy crust.",
                        cost=205))
    db.session.add(Dish(name="Four-Cheese White Pizza", description="Pepper jack, parmesan, white cheddar, and feta cheese with white sauce, all on a "
                        + "thin, crispy crust with pesto drizzled over it.",
                        cost=255))
    db.session.add(Dish(name="Pepperoni Pizza", description="Pepperoni and cheese with marinara sauce, all on a "
                        + "thin, crispy crust.",
                        cost=891))
    db.session.add(Drink(name="Seventh Heaven", description="This energizing drink that packs a serious punch" +
                         " consists of gin, maraschino liqueur, and grapefruit juice!", type="Cocktail", cost=600))
    db.session.add(Drink(name="Cosmo Canyon", description="A drink that'll remind you of the very place it's named after!  " +
                         "Contains citrus vodka, cointreau, lime juice, and cranberry juice.", type="Cocktail", cost=600))
    db.session.add(Drink(name="Lifestream", description="A cocktail that'll breathe new life into you!  " +
                         "Contains Barcardi lemon, peppermint green, apple juice, and lime.", type="Cocktail", cost=600))
    db.session.add(Drink(name="Rainbow Wine", description="Ever made wine with rainbow grapes?  It's a fruity taste like no other!", 
                         type="Wine", cost=700))
    db.session.add(Drink(name="Draft Beer", description="Fresh beer served in a keg!", 
                         type="Beer", cost=600))
    db.session.add(Drink(name="Rum & Cola", description="Sometimes, two classics mixed together is all you need.", 
                         type="Cocktail", cost=600))
    db.session.add(Drink(name="Sex on Costa del Sol", description="Vodka, peach schnapps, cranberry juice, and orange juice.", 
                         type="Cocktail", cost=600))
    db.session.add(Drink(name="Seven SOLDIERS", description="Red and white wine blend with a pinch of cinnamon for a kick.", type="Wine", cost=600))
    db.session.add(Drink(name="Cosmo Road", description="This red wine is out of this world!", type="Wine", cost=600))
    db.session.add(Drink(name="Blue Moogle", description="A citrusy beer that tastes about half as sweet as its name!", type="Beer", cost=600))
    db.session.add(Drink(name="Midgar Ultra", description="Midgar is home to this crisp, light beer.", type="Beer", cost=600))
    db.session.add(Drink(name="Wutai Brut", description="A champagne made from premium grapes only found in Wutai!", type="Wine", cost=600))
    db.session.add(Drink(name="Classic Coffee", description="Ready to start your day?  Just say how much cream and sugar you want, and you got it!", type="Non-Alcoholic", cost=400))
    db.session.add(Drink(name="Hot Chocolate", description="A classic beverage to drink on a cold winter day.  Or just any day!  Served with whipped cream. and marshmallows", type="Non-Alcoholic", cost=400))
    db.session.add(Drink(name="Apple Cider", description="A classic beverage to drink on a cool autumn day.  Or just any day!", type="Non-Alcoholic", cost=400))
    db.session.add(Drink(name="Green Tea", description="A healthy warm drink that'll leave you feeling relaxed!", type="Non-Alcoholic", cost=400))
    db.session.add(Drink(name="Boba Milk Tea", description="A sweet brown sugar tea with tapioca pearls inside!", type="Non-Alcoholic", cost=400))
    db.session.query(Drink).order_by(Drink.type.desc())
    db.session.add(Article(title="Moving Forward", date="December 12 [ν] – εγλ 0007"))
    db.session.add(Article(title="In Loving Memory of Aerith Gainsborough", date="December 21 [ν] – εγλ 0007"))
    db.session.add(Article(title="New Seventh Heaven Built in Edge", date="August 7 [ν] – εγλ 0008"))
    db.session.commit()"""
    


@app.route('/')
def index():
    return render_template("home.j2", name="Home", button_titles = button_titles)

@app.route('/home')
def redirect_home():
    return redirect("/")

@app.route('/menu')
def menu():
    dishes = Dish.query.all()
    drinks = Drink.query.order_by(Drink.type.asc())
    return render_template("menu.j2", name="Menu", button_titles = button_titles, dishes=dishes, drinks=drinks)


@app.route('/news')
def news():
    articles = Article.query.order_by(Article.id.desc())
    return render_template("news.j2", name="News", button_titles = button_titles, articles=articles)

@app.route('/news/moving-forward')
def moving_forward():
    return render_template("7heavendestroyed.j2", button_titles = button_titles)

@app.route('/news/in-loving-memory-of-aerith-gainsborough')
def in_loving_memory():
    return render_template("ripaerith.j2", button_titles = button_titles)

@app.route('/news/new-seventh-heaven-built-in-edge')
def new_seventh_heaven():
    return render_template("new7heaven.j2", button_titles = button_titles)

@app.route('/contact-us')
def contact():
    return render_template("contactus.j2", button_titles = button_titles)