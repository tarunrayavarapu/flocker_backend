# Home Page Channels
general = Group.query.filter_by(name='General').first()
support = Group.query.filter_by(name='Support').first()
home_page_channels = [
    Channel(name='Announcements', group_id=general.id),
    Channel(name='Events', group_id=general.id),
    Channel(name='FAQ', group_id=support.id),
    Channel(name='Help Desk', group_id=support.id)
]

# Shared Interest Channels
limitless_connection = Group.query.filter_by(name='Limitless Connections').first() 
dnhs_football = Group.query.filter_by(name='DNHS Football').first() 
school_subjects = Group.query.filter_by(name='School Subjects').first()
music = Group.query.filter_by(name='Music').first()
satire = Group.query.filter_by(name='Satire').first()
activity_hub = Group.query.filter_by(name='Activity Hub').first()
shared_interest_channels = [
    Channel(name='Penpal Letters', group_id=limitless_connection.id),
    Channel(name='Game vs Poway', group_id=dnhs_football.id),
    Channel(name='Game vs Westview', group_id=dnhs_football.id),
    Channel(name='Math', group_id=school_subjects.id),
    Channel(name='English', group_id=school_subjects.id),
    Channel(name='Artist', group_id=music.id),
    Channel(name='Music Genre', group_id=music.id),
    Channel(name='Humor', group_id=satire.id),
    Channel(name='Memes', group_id=satire.id),
    Channel(name='Irony', group_id=satire.id),
    Channel(name='Cyber Patriots', group_id=activity_hub.id),
    Channel(name='Robotics', group_id=activity_hub.id)
]

# Create and Compete Channels
riddle_creators = Group.query.filter_by(name='Riddle Creators').first()
competition_central = Group.query.filter_by(name='Competition Central').first()
puzzle_showdowns = Group.query.filter_by(name='Puzzle Showdowns').first()
create_compete_channels = [
    Channel(name='New Ideas', group_id=riddle_creators.id),
    Channel(name='Submission Guidelines', group_id=riddle_creators.id),
    Channel(name='Current Challenges', group_id=competition_central.id),
    Channel(name='Past Winners', group_id=puzzle_showdowns.id),
    Channel(name='Upcoming Showdowns', group_id=puzzle_showdowns.id)
]

# Vote for the GOAT Channels
best_riddles = Group.query.filter_by(name='Best Riddles').first()
top_solvers = Group.query.filter_by(name='Top Solvers').first()
goat_polls = Group.query.filter_by(name='GOAT Polls').first()
vote_goat_channels = [
    Channel(name='Top Riddles', group_id=best_riddles.id),
    Channel(name='Hall of Fame', group_id=top_solvers.id),
    Channel(name='Community Votes', group_id=goat_polls.id)
]

# Share and Care Channels
hint_exchange = Group.query.filter_by(name='Hint Exchange').first()
collaboration_corner = Group.query.filter_by(name='Collaboration Corner').first()
guidance_tips = Group.query.filter_by(name='Guidance and Tips').first()
share_care_channels = [
    Channel(name='Helpful Hints', group_id=hint_exchange.id),
    Channel(name='Teamwork Strategies', group_id=collaboration_corner.id),
    Channel(name='Riddle Tutorials', group_id=guidance_tips.id)
]

# Rate and Relate Channels
riddle_ratings = Group.query.filter_by(name='Riddle Ratings').first()
feedback_forum = Group.query.filter_by(name='Feedback Forum').first()
reflection_zone = Group.query.filter_by(name='Reflection Zone').first()
rate_relate_channels = [
    Channel(name='Rate the Riddle', group_id=riddle_ratings.id),
    Channel(name='Community Feedback', group_id=feedback_forum.id),
    Channel(name='Discussion & Insights', group_id=reflection_zone.id)
]

# Consolidate all channels
channels = home_page_channels + shared_interest_channels + create_compete_channels + vote_goat_channels + share_care_channels + rate_relate_channels
