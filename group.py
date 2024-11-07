# Home Page Groups
home_page_section = Section.query.filter_by(name='Home Page').first()
groups = [
    Group(name='General', section_id=home_page_section.id, moderators=[User.query.get(1)]),
    Group(name='Support', section_id=home_page_section.id, moderators=[User.query.get(1)])
]

# Shared Interest Groups
shared_interest_section = Section.query.filter_by(name='Shared Interest').first()
groups += [
    Group(name='Limitless Connections', section_id=shared_interest_section.id, moderators=[User.query.get(1)]),
    Group(name='DNHS Football', section_id=shared_interest_section.id, moderators=[User.query.get(1)]),
    Group(name='School Subjects', section_id=shared_interest_section.id, moderators=[User.query.get(1)]),
    Group(name='Music', section_id=shared_interest_section.id, moderators=[User.query.get(1)]),
    Group(name='Satire', section_id=shared_interest_section.id, moderators=[User.query.get(1)]),
    Group(name='Activity Hub', section_id=shared_interest_section.id, moderators=[User.query.get(1)])
]

# Create and Compete Groups
create_compete_section = Section.query.filter_by(name='Create and Compete').first()
groups += [
    Group(name='Riddle Creators', section_id=create_compete_section.id, moderators=[User.query.get(1)]),
    Group(name='Competition Central', section_id=create_compete_section.id, moderators=[User.query.get(1)]),
    Group(name='Puzzle Showdowns', section_id=create_compete_section.id, moderators=[User.query.get(1)])
]

# Vote for the GOAT Groups
vote_goat_section = Section.query.filter_by(name='Vote for the GOAT').first()
groups += [
    Group(name='Best Riddles', section_id=vote_goat_section.id, moderators=[User.query.get(1)]),
    Group(name='Top Solvers', section_id=vote_goat_section.id, moderators=[User.query.get(1)]),
    Group(name='GOAT Polls', section_id=vote_goat_section.id, moderators=[User.query.get(1)])
]

# Share and Care Groups
share_care_section = Section.query.filter_by(name='Share and Care').first()
groups += [
    Group(name='Hint Exchange', section_id=share_care_section.id, moderators=[User.query.get(1)]),
    Group(name='Collaboration Corner', section_id=share_care_section.id, moderators=[User.query.get(1)]),
    Group(name='Guidance and Tips', section_id=share_care_section.id, moderators=[User.query.get(1)])
]

# Rate and Relate Groups
rate_relate_section = Section.query.filter_by(name='Rate and Relate').first()
groups += [
    Group(name='Riddle Ratings', section_id=rate_relate_section.id, moderators=[User.query.get(1)]),
    Group(name='Feedback Forum', section_id=rate_relate_section.id, moderators=[User.query.get(1)]),
    Group(name='Reflection Zone', section_id=rate_relate_section.id, moderators=[User.query.get(1)])
]
