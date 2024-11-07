# app.py

from flask import Flask, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
from riddle_module import RiddleCollection

app = Flask(__name__)
scheduler = BackgroundScheduler()
riddle_collection = RiddleCollection()  # Initialize the riddle collection

# Route to get a random riddle
@app.route('/riddle', methods=['GET'])
def get_riddle():
    riddle = riddle_collection.get_random_riddle()
    return jsonify({"question": riddle.question, "answer": riddle.answer})

# Function to post a random riddle every 24 hours (or use it however you like)
def post_random_riddle():
    riddle = riddle_collection.get_random_riddle()
    print(f"Riddle of the day: {riddle.question}")
    print(f"Answer: {riddle.answer}")

# Scheduler to run post_random_riddle every 24 hours
scheduler.add_job(post_random_riddle, 'interval', hours=24)
scheduler.start()

if __name__ == '__main__':
    app.run()
