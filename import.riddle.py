import random
from flask_sqlalchemy import SQLAlchemy
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

db = SQLAlchemy()

class Riddle(db.Model):
    """
    Riddle Model to store riddles in the database.

    Attributes:
        id (int): Primary key, unique identifier for the riddle.
        question (str): The riddle question.
        answer (str): The answer to the riddle.
        posted_at (datetime): Timestamp when the riddle was last posted.
    """
    __tablename__ = 'riddles'

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(255), nullable=False)
    answer = db.Column(db.String(255), nullable=False)
    posted_at = db.Column(db.DateTime, nullable=True)  # Keeps track of when the riddle was posted

    def __init__(self, question, answer):
        self.question = question
        self.answer = answer

    def __repr__(self):
        return f"<Riddle(id={self.id}, question='{self.question}', answer='{self.answer}')>"

    def mark_as_posted(self):
        """
        Marks the riddle as posted by setting the `posted_at` timestamp to now.
        """
        self.posted_at = datetime.utcnow()
        db.session.commit()

# Function to initialize the database with some sample riddles
def init_riddles():
    """
    Initializes the Riddle table with sample riddles.
    """
    db.create_all()

    sample_riddles = [
        Riddle(question="What has keys but can't open locks?", answer="A piano"),
        Riddle(question="What runs but never walks?", answer="A river"),
        Riddle(question="I speak without a mouth and hear without ears. What am I?", answer="An echo"),
        Riddle(question="The more you take, the more you leave behind. What am I?", answer="Footsteps")
    ]

    for riddle in sample_riddles:
        db.session.add(riddle)
    db.session.commit()
    print("Sample riddles have been added.")

# Function to post a random riddle every 24 hours
def post_random_riddle():
    """
    Selects a random riddle from the database, marks it as the "riddle of the day,"
    and updates the posted timestamp.
    """
    riddles = Riddle.query.all()
    if riddles:
        selected_riddle = random.choice(riddles)
        selected_riddle.mark_as_posted()
        print(f"Riddle of the Day: {selected_riddle.question}")

# Setup the scheduler
def start_scheduler(app):
    """
    Starts a background scheduler to post a random riddle every 24 hours.

    Args:
        app: Flask application instance.
    """
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=post_random_riddle, trigger="interval", hours=24)

    # Start the scheduler in the app context
    with app.app_context():
        scheduler.start()
    print("Scheduler started: posting a riddle every 24 hours.")

    # Shut down the scheduler when exiting the app
    app.teardown_appcontext(lambda exception: scheduler.shutdown())

# riddle_module.py

import random

class Riddle:
    """
    Riddle Class
    
    This class represents a riddle with a question and an answer.
    
    Attributes:
        question (str): The riddle question.
        answer (str): The answer to the riddle.
    """
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer

    def __repr__(self):
        return f"Riddle(question='{self.question}', answer='{self.answer}')"


class RiddleCollection:
    """
    RiddleCollection Class
    
    Manages a collection of riddles and allows for retrieval of random riddles.
    """
    def __init__(self):
        # Initialize the collection of riddles
        self.riddles = [
            Riddle("I am thought to be everywhere, and I only have one rival. He hides within himself, and stays wherever I cannot reach. Who am I? And who is my rival?", "Light and Darkness"),
            Riddle("The more of this there is, the less you see. What is it?", "Darkness"),
            Riddle("What has keys but can't open locks?", "A piano"),
            Riddle("I'm tall when I'm young and short when I'm old. What am I?", "A candle"),
            Riddle("What comes once in a minute, twice in a moment, but never in a thousand years?", "The letter M"),
            Riddle("Forward I am heavy, but backward I am not. What am I?", "The word 'ton'"),
            Riddle("I have branches, but no fruit, trunk, or leaves. What am I?", "A bank"),
        ]

    def get_random_riddle(self):
        """
        Selects a random riddle from the collection.

        Returns:
            Riddle: A randomly selected Riddle object.
        """
        return random.choice(self.riddles)

    def add_riddle(self, question, answer):
        """
        Adds a new riddle to the collection.

        Args:
            question (str): The riddle question.
            answer (str): The riddle answer.
        """
        new_riddle = Riddle(question, answer)
        self.riddles.append(new_riddle)
        print(f"Riddle added: {new_riddle}")

    def get_all_riddles(self):
        """
        Returns all riddles in the collection.

        Returns:
            list: A list of Riddle objects.
        """
        return self.riddles
