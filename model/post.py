# post.py
from sqlite3 import IntegrityError
from sqlalchemy import Text
from __init__ import app, db
from model.user import User
from model.group import Group

class Post(db.Model):
    """
    Post Model
    
    The Post class represents an individual contribution or discussion within a group.
    
    Attributes:
        id (db.Column): The primary key, an integer representing the unique identifier for the post.
        _title (db.Column): A string representing the title of the post.
        _content (db.Column): A Text blob representing the content of the post.
        _user_id (db.Column): An integer representing the user who created the post.
        _group_id (db.Column): An integer representing the group to which the post belongs.
    """
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    _title = db.Column(db.String(255), nullable=False)
    _content = db.Column(Text, nullable=False)
    _user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    _group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)

    def __init__(self, title, content, user_id, group_id):
        self._title = title
        self._content = content
        self._user_id = user_id
        self._group_id = group_id

    def __repr__(self):
        return f"Post(id={self.id}, title={self._title}, content={self._content}, user_id={self._user_id}, group_id={self._group_id})"

    def create(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
        
    # CRUD read converts self to dictionary
    # returns dictionary
    def read(self):
        user = User.query.get(self._user_id)
        group = Group.query.get(self._group_id)
        data = {
            "id": self.id,
            "title": self._title,
            "content": self._content,
            "user_name": user.name if user else None,
            "group_name": group.name if group else None
        }
        return data
    
    def update(self):
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
        
    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
        
def initPosts():
    with app.app_context():
        """Create database and tables"""
        db.create_all()
        """Tester data for table"""
        
        p1 = Post(title='Calculus Help', content='Need help with derivatives.', user_id=1, group_id=1)  
        p2 = Post(title='Game Day', content='Who is coming to the game?', user_id=2, group_id=2)
        p3 = Post(title='New Releases', content='What movies are you excited for?', user_id=3, group_id=3)
        p4 = Post(title='Study Group', content='Meeting at the library.', user_id=1, group_id=1)
        
        for post in [p1, p2, p3, p4]:
            try:
                post.create()
            except IntegrityError:
                '''fails with bad or duplicate data'''
                db.session.remove()
                print(f"Records exist, duplicate email, or error: {post.uid}")