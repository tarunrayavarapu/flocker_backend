# group.py
from sqlite3 import IntegrityError
from __init__ import app, db
from model.user import User

# Association table for the many-to-many relationship between Group and User (moderators)
group_moderators = db.Table('group_moderators',
    db.Column('group_id', db.Integer, db.ForeignKey('groups.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
)

class Group(db.Model):
    """
    Group Model
    
    The Group class represents a specific community within a section.
    
    Attributes:
        id (db.Column): The primary key, an integer representing the unique identifier for the group.
        _name (db.Column): A string representing the name of the group.
        _section_id (db.Column): An integer representing the section to which the group belongs.
        moderators (relationship): A collection of users who are the moderators of the group.
    """
    __tablename__ = 'groups'

    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String(255), unique=True, nullable=False)
    _section_id = db.Column(db.Integer, db.ForeignKey('sections.id'), nullable=False)

    channels = db.relationship('Channel', backref='group', lazy=True)
    moderators = db.relationship('User', secondary=group_moderators, lazy='subquery',
                                 backref=db.backref('moderated_groups', lazy=True))
    
    def __init__(self, name, section_id, moderators=None):
        """
        Constructor, 1st step in object creation.
        
        Args:
            name (str): The name of the group.
            section_id (int): The section to which the group belongs.
            moderators (list, optional): A list of users who are the moderators of the group. Defaults to None.
        """
        self._name = name
        self._section_id = section_id
        self.moderators = moderators or []
        
    @property
    def name(self):
        """
        Gets the group's name.
        
        Returns:
            str: The group's name.
        """
        return self._name

    def __repr__(self):
        """
        The __repr__ method is a special method used to represent the object in a string format.
        Called by the repr() built-in function.
        
        Returns:
            str: A text representation of how to create the object.
        """
        return f"Group(id={self.id}, name={self._name}, section_id={self._section_id}, moderators={[moderator.id for moderator in self.moderators]})"

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
        
        Returns:
            dict: A dictionary containing the group data.
        """
        return {
            'id': self.id,
            'name': self._name,
            'section_id': self._section_id,
            'moderators': [moderator.id for moderator in self.moderators]
        }
        
def initGroups():
    """
    The initGroups function creates the Group table and adds tester data to the table.
    
    Uses:
        The db ORM methods to create the table.
    
    Instantiates:
        Group objects with tester data.
    
    Raises:
        IntegrityError: An error occurred when adding the tester data to the table.
    """
    with app.app_context():
        """Create database and tables"""
        db.create_all()
        """Tester data for table"""
        
        g1 = Group(name='Limitless Connections', section_id=1, moderators=[User.query.get(1)])
        g2 = Group(name='DNHS Football', section_id=1, moderators=[User.query.get(1)])
        g3 = Group(name='School Subjects', section_id=1, moderators=[User.query.get(1)])
        g4 = Group(name='Music', section_id=1, moderators=[User.query.get(1)])
        g5 = Group(name='Satire', section_id=1, moderators=[User.query.get(1)])
        g6 = Group(name='Activity Hub', section_id=1, moderators=[User.query.get(1)])

        groups = [g1, g2, g3, g4, g5, g6]
        for group in groups:
            try:
                group.create()
            except IntegrityError:
                '''fails with bad or duplicate data'''
                db.session.remove()
                print(f"Records exist, duplicate email, or error: {group._name}")