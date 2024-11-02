# post.py
from sqlite3 import IntegrityError
from sqlalchemy import Text, JSON
from __init__ import app, db
from model.user import User
from model.channel import Channel

class Post(db.Model):
    """
    Post Model
    
    The Post class represents an individual contribution or discussion within a channel.
    
    Attributes:
        id (db.Column): The primary key, an integer representing the unique identifier for the post.
        _title (db.Column): A string representing the title of the post.
        _content (db.Column): A JSON blob representing the content of the post.
        _user_id (db.Column): An integer representing the user who created the post.
        _channel_id (db.Column): An integer representing the channel to which the post belongs.
    """
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    _title = db.Column(db.String(255), nullable=False)
    _content = db.Column(JSON, nullable=False)
    _user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    _channel_id = db.Column(db.Integer, db.ForeignKey('channels.id'), nullable=False)

    def __init__(self, title, content, user_id, channel_id):
        """
        Constructor, 1st step in object creation.
        
        Args:
            title (str): The title of the post.
            content (dict): The content of the post.
            user_id (int): The user who created the post.
            channel_id (int): The channel to which the post belongs.
        """
        self._title = title
        self._content = content
        self._user_id = user_id
        self._channel_id = channel_id

    def __repr__(self):
        """
        The __repr__ method is a special method used to represent the object in a string format.
        Called by the repr(post) built-in function, where post is an instance of the Post class.
        
        Returns:
            str: A text representation of how to create the object.
        """
        return f"Post(id={self.id}, title={self._title}, content={self._content}, user_id={self._user_id}, channel_id={self._channel_id})"

    def create(self):
        """
        The create method adds the object to the database and commits the transaction.
        
        Uses:
            The db ORM methods to add and commit the transaction.
        
        Raises:
            Exception: An error occurred when adding the object to the database.
        """
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
        
    def read(self):
        """
        The read method retrieves the object data from the object's attributes and returns it as a dictionary.
        
        Uses:
            The Channel.query and User.query methods to retrieve the channel and user objects.
        
        Returns:
            dict: A dictionary containing the post data, including user and channel names.
        """
        user = User.query.get(self._user_id)
        channel = Channel.query.get(self._channel_id)
        data = {
            "id": self.id,
            "title": self._title,
            "content": self._content,
            "user_name": user.name if user else None,
            "channel_name": channel.name if channel else None
        }
        return data
    
    def update(self):
        """
        The update method commits the transaction to the database.
        
        Uses:
            The db ORM method to commit the transaction.
        
        Raises:
            Exception: An error occurred when updating the object in the database.
        """
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
    
    def delete(self):
        """
        The delete method removes the object from the database and commits the transaction.
        
        Uses:
            The db ORM methods to delete and commit the transaction.
        
        Raises:
            Exception: An error occurred when deleting the object from the database.
        """    
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

def initPosts():
    """
    The initPosts function creates the Post table and adds tester data to the table.
    
    Uses:
        The db ORM methods to create the table.
    
    Instantiates:
        Post objects with tester data.
    
    Raises:
        IntegrityError: An error occurred when adding the tester data to the table.
    """        
    with app.app_context():
        """Create database and tables"""
        db.create_all()
        """Tester data for table"""
        
        p1 = Post(title='Penpal Letter', content={'comment': 'Looking forward to your reply!'}, user_id=1, channel_id=1)
        p2 = Post(title='Game vs Poway', content={'comment': 'Excited for the game!'}, user_id=2, channel_id=2)
        p3 = Post(title='Game vs Westview', content={'comment': 'Ready to win!'}, user_id=2, channel_id=3)
        p4 = Post(title='Math Homework', content={'comment': 'Need help with derivatives.'}, user_id=3, channel_id=4)
        p5 = Post(title='English Essay', content={'comment': 'Struggling with my essay.'}, user_id=3, channel_id=5)
        p6 = Post(title='Favorite Artist', content={'comment': 'I love this artist!'}, user_id=4, channel_id=6)
        p7 = Post(title='Music Genre', content={'comment': 'What genre do you like?'}, user_id=4, channel_id=7)
        p8 = Post(title='Humor', content={'comment': 'Share your funniest jokes!'}, user_id=5, channel_id=8)
        p9 = Post(title='Memes', content={'comment': 'Post your favorite memes!'}, user_id=5, channel_id=9)
        p10 = Post(title='Irony', content={'comment': 'Discuss ironic situations.'}, user_id=5, channel_id=10)
        p11 = Post(title='Cyber Patriots', content={'comment': 'Join the team!'}, user_id=6, channel_id=11)
        p12 = Post(title='Robotics', content={'comment': 'Building a new robot.'}, user_id=6, channel_id=12)
        
        posts = [p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12]
        for post in posts:
            try:
                post.create()
                print(f"Record created: {repr(post)}")
            except IntegrityError:
                '''fails with bad or duplicate data'''
                db.session.remove()
                print(f"Records exist, duplicate email, or error: {post._title}")