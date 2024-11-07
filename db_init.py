from flask import Flask
from riddle_module import db, init_riddles, start_scheduler

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///riddles.db'
db.init_app(app)

with app.app_context():
    init_riddles()  # Initialize sample riddles in the database
    start_scheduler(app)  # Start the scheduler
