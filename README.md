Visit the website here! http://tifalockhart07.pythonanywhere.com/

This is a website for the fictional bar, Seventh Heaven, from the video game, Final Fantasy 7!  This is a 90's-styled website, since Final Fantasy 7 came out in 1997.  I plan to create a modern version of this website in the near future.

## Overview

**Home**

This section describes Seventh Heaven and an overview of what it has to offer, along with information about Tifa Lockhart, the owner of Seventh Heaven, and Cloud Strife, Tifa's friend who, for some reason, has his own section.

**Menu**

This page displays menu items extracted from an SQLAlchemy database.  The drinks are sorted by type in alphabetical order.  I decided to display the food and drink menus side by side to reduce the amount of scrolling required.

**News**

This page displays links to news articles, also extracted from an SQLAlchemy database sorted by date.  Because these dates use a fictional calendar system, I sorted them by ID and added the articles in order.

**Contact**

There's not much here, just an e-mail address, the bar's hours of operation, and the address of the location.


If you would like to download this website and experiment with it, here's how you can run it!

## How to Run

1. Open VS Code
2. Open the terminal in the IDE
3. If you don't have flask installed, run `pip install flask`
4. If you don't have SQLAlchemy installed, run `pip install flask-sqlalchemy`
5. Finally, to run the software, run `pythom -m flask --app home run`
