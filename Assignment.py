import re


class Assignment:
    def __init__(self, assignment, courses, db):
        self.course = courses[assignment['course_id']]
        self.id = assignment['id']
        self.name = assignment['name']
        self.status = "To Do"
        self.description = self.cleanhtml(assignment['description'])
        self.due_at_date = assignment['due_at_date']
        self.html_url = assignment['html_url']
        self.assignment_type = "Uncategorized"
        self.db = db

    def cleanhtml(self, raw_html):
        # cleanr = re.compile('<.*?>')
        cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
        cleantext = re.sub(cleanr, '', raw_html)
        return cleantext

    # def create_query(self, entry):
