import re
from datetime import datetime, timezone
from time import strftime
import config as config
import pytz

from util import cleanhtml, format_course_name
class Assignment:
    def __init__(self, assignment, course_name):
        self.course_name = format_course_name(course_name)
        self.id = assignment['id']
        self.name = assignment['name']
        self.status = "Not Started"
        self.description = assignment['description'][0:2000]
        self.due_at_date = datetime.now() if not isinstance(assignment['due_at_date'], datetime) else assignment['due_at_date']
        self.html_url = assignment['html_url']
        self.assignment_type = self.__get_assignment_type(assignment)

    def __get_assignment_type(self, assignment):
        if isinstance(assignment['due_at_date'], datetime):
            return "Quiz" if assignment['is_quiz_assignment'] else "Assignment"
        else:
            return "Quiz" if assignment['is_quiz_assignment'] else "Event"

        

    def create_notion_page(self):
        new_page = {
                "Assignment ID" : {"type": "number", "number" : self.id},
                "Name" : {"type": "title", "title": [{"type": "text", "text": {"content": self.name}}]},
                "Status" : {"type": "status", "status": {"name": "Not Started"}},
                "Class" : {"type": "select", "select": {"name": self.course_name}},
                "Assignment Type" : {"type": "select", "select": {"name": self.assignment_type}},
                "Due Date" : {"type" : "date", "date" : {"start": self.due_at_date.astimezone(pytz.timezone('US/Eastern')).strftime('%Y-%m-%dT%H:%M:%S'), "time_zone": "America/New_York"}},
                "Link" : {"type" : "url", "url" : self.html_url}
        }

        children = [
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                "rich_text": [{ "type": "text", "text": { "content": cleanhtml(self.description)} }]
                }
            }
        ]
        return new_page, children
