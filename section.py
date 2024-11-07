class Section:
    def __init__(self, name):
        self.name = name

# Define the sections of the riddle room experience
home_page = Section(name='Home Page')            # Introductory area or starting point
shared_interest = Section(name='Shared Interest') # Room for common themes or clues
create_compete = Section(name='Create and Compete') # Puzzle creation or challenge area
vote_goat = Section(name='Vote for the GOAT')     # Vote on the best solvers or riddles
share_care = Section(name='Share and Care')       # Area to share hints or insights
rate_relate = Section(name='Rate and Relate')     # Section to rate riddles or provide feedback

riddle_room_sections = [home_page, shared_interest, create_compete, vote_goat, share_care, rate_relate]
