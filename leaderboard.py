from datetime import datetime
from config import db  # Import your configured db instance
from sqlalchemy.exc import IntegrityError

class RiddleLeaderboardEntry(db.Model):
    """
    RiddleLeaderboardEntry Model
    Represents a single entry in the leaderboard, tracking user points for correctly answering riddles.
    
    Attributes:
        id (db.Column): Primary key representing the unique identifier for the leaderboard entry.
        user_id (db.Column): Foreign key ID of the user associated with this entry.
        correct_answers (db.Column): Integer count of correct riddle answers by the user.
        total_attempts (db.Column): Integer count of all attempts made by the user.
        points (db.Column): Calculated points for the user on the leaderboard.
        last_updated (db.Column): Datetime of the last update to this leaderboard entry.
    """
    __tablename__ = 'riddle_leaderboard'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    correct_answers = db.Column(db.Integer, default=0)
    total_attempts = db.Column(db.Integer, default=0)
    points = db.Column(db.Float, default=0.0)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, user_id, correct_answers=0, total_attempts=0, points=0.0):
        """
        Constructor for initializing a RiddleLeaderboardEntry object.
        
        Args:
            user_id (int): ID of the user for this leaderboard entry.
            correct_answers (int): Number of correct answers by the user.
            total_attempts (int): Total number of attempts by the user.
            points (float): Points awarded based on correct answers.
        """
        self.user_id = user_id
        self.correct_answers = correct_answers
        self.total_attempts = total_attempts
        self.points = points

    def __repr__(self):
        """
        Returns a string representation of the RiddleLeaderboardEntry object.
        
        Returns:
            str: Text representation of the RiddleLeaderboardEntry.
        """
        return f"RiddleLeaderboardEntry(id={self.id}, user_id={self.user_id}, points={self.points})"

    def save(self):
        """
        Saves the RiddleLeaderboardEntry object to the database.
        
        Raises:
            Exception: Rolls back the transaction if an error occurs.
        """
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def update_points(self):
        """
        Updates the points based on correct answers and total attempts.
        Points are calculated as the ratio of correct answers to total attempts, multiplied by a reward factor.
        
        Raises:
            Exception: Rolls back the transaction if an error occurs.
        """
        try:
            reward_factor = 10  # Points per correct answer
            self.points = self.correct_answers * reward_factor
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

def init_riddle_leaderboard():
    """
    Initializes the Riddle Leaderboard table with sample data for testing.
    
    Uses:
        SQLAlchemy ORM to create the table and add sample leaderboard entries.
    
    Instantiates:
        RiddleLeaderboardEntry objects with sample data.
    
    Raises:
        IntegrityError: Occurs if there are duplicate or invalid data entries.
    """
    with app.app_context():
        # Create the Riddle Leaderboard table
        db.create_all()
        
        # Sample leaderboard entries for testing
        entry1 = RiddleLeaderboardEntry(user_id=1, correct_answers=3, total_attempts=5)
        entry2 = RiddleLeaderboardEntry(user_id=2, correct_answers=5, total_attempts=8)

        for entry in [entry1, entry2]:
            try:
                entry.update_points()  # Update points based on correct answers
                entry.save()  # Save to the database
                print(f"Record created: {repr(entry)}")
            except IntegrityError:
                db.session.rollback()
                print(f"Error: Duplicate or invalid data for leaderboard entry for user {entry.user_id}")
