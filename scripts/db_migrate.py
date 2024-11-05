#!/usr/bin/env python3

""" db_migrate.py
Generates the database schema for all db models
- Initializes Users, Sections, and UserSections tables.
- Imports data from the old database to the new database.

Usage: Run from the terminal as such:

Goto the scripts directory:
> cd scripts; ./db_migrate.py

Or run from the root of the project:
> scripts/db_migrate.py

General Process outline:
0. Warning to the user.
1. Old data extraction.  An API has been created in the old project ...
  - Extract Data: retrieves data from the specified tables in the old database.
  - Transform Data: the API to JSON format understood by the new project.
2. New schema.  The schema is created in "this" new database.
3. Load Data: The bulk load API in "this" project inserts the data using required business logic.

"""
import shutil
import sys
import os
import json

# Add the directory containing main.py to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# Import application object
from main import app, db, generate_data
from model.user import User
from model.section import Section
from model.group import Group
from model.channel import Channel
from model.post import Post

# Backup the old database
def backup_database(db_uri, backup_uri):
    """Backup the current database."""
    if backup_uri:
        db_path = db_uri.replace('sqlite:///', 'instance/')
        backup_path = backup_uri.replace('sqlite:///', 'instance/')
        shutil.copyfile(db_path, backup_path)
        print(f"Database backed up to {backup_path}")
    else:
        print("Backup not supported for production database.")

# Extract data from the existing database
def extract_data():
    data = {}
    with app.app_context():
        data['users'] = [user.read() for user in User.query.all()]
        data['sections'] = [section.read() for section in Section.query.all()]
        data['groups'] = [group.read() for group in Group.query.all()]
        data['channels'] = [channel.read() for channel in Channel.query.all()]
        data['posts'] = [post.read() for post in Post.query.all()]
    return data

# Save extracted data to JSON files
def save_data_to_json(data, directory='backup'):
    if not os.path.exists(directory):
        os.makedirs(directory)
    for table, records in data.items():
        with open(os.path.join(directory, f'{table}.json'), 'w') as f:
            json.dump(records, f)
    print(f"Data backed up to {directory} directory.")

# Load data from JSON files
def load_data_from_json(directory='backup'):
    data = {}
    for table in ['users', 'sections', 'groups', 'channels', 'posts']:
        with open(os.path.join(directory, f'{table}.json'), 'r') as f:
            data[table] = json.load(f)
    return data

# Restore data to the new database
def restore_data(data):
    with app.app_context():
        for user_data in data['users']:
            user = User(**user_data)
            db.session.add(user)
        for section_data in data['sections']:
            section = Section(**section_data)
            db.session.add(section)
        for group_data in data['groups']:
            group = Group(**group_data)
            db.session.add(group)
        for channel_data in data['channels']:
            channel = Channel(**channel_data)
            db.session.add(channel)
        for post_data in data['posts']:
            post = Post(**post_data)
            db.session.add(post)
        db.session.commit()
    print("Data restored to the new database.")

# Main extraction and loading process
def main():
    
    # Step 0: Warning to the user and backup table
    with app.app_context():
        try:
            # Step 3: Build New schema
            # Check if the database has any tables
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            
            if tables:
                print("Warning, you are about to lose all data in the database!")
                print("Do you want to continue? (y/n)")
                response = input()
                if response.lower() != 'y':
                    print("Exiting without making changes.")
                    sys.exit(0)
                    
            # Backup the old database
            backup_database(app.config['SQLALCHEMY_DATABASE_URI'], app.config['SQLALCHEMY_BACKUP_URI'])
           
        except Exception as e:
            print(f"An error occurred: {e}")
            sys.exit(1)
        
    # Step 1: Extract and save existing data
    try:
        data = extract_data()
        save_data_to_json(data)
    except Exception as e:
        print(f"An error occurred during data extraction: {e}")
        sys.exit(1)
    
    # Step 2: Build New schema and create test data 
    try:
        with app.app_context():
            # Drop all the tables defined in the project
            db.drop_all()
            print("All tables dropped.")
            
            # Create the tables defined in the project
            print("Generating data.")
            generate_data()
                        
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
    
    # Step 3: Restore data to the new database
    try:
        data = load_data_from_json()
        restore_data(data)
    except Exception as e:
        print(f"An error occurred during data restoration: {e}")
        sys.exit(1)
    
    # Log success 
    print("Database initialized!")
 
if __name__ == "__main__":
    main()