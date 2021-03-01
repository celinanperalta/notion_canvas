from canvasapi import Canvas
from canvasapi import assignment
from notion.client import NotionClient
import config as config
import re
from datetime import datetime, timezone

# Get current classes


class AssignmentDB:
    def __init__(self):
        self.canvas = Canvas(config.CANVAS_API_URL, config.CANVAS_API_KEY)
        self.user = self.canvas.get_user(config.CANVAS_USER_ID)
        self.courses = self.user.get_courses(enrollment_state='active')
        self.current_courses = self.get_current_courses()
        self.assignment_list = self.get_current_assignments()

        self.client = NotionClient(config.NOTION_TOKEN)
        self.cv = self.client.get_collection_view(config.NOTION_LINK)

    def get_current_courses(self):
        current_classes = {}
        for course in self.courses:
            if (hasattr(course, 'enrollment_term_id') and course.enrollment_term_id == config.CANVAS_ENROLLMENT_TERM):
                course_name = "".join(course.name[6:14].split())
                print(course_name + " " + str(course.id))
                current_classes[course.id] = course_name
        return current_classes

    # Get current assignments given list of courses
    def get_current_assignments(self):
        current_assignments = {}
        assignment_attrs = ['name', 'description',
                            'due_at_date', 'course_id', 'id', 'html_url', 'locked_for_user', 'has_submitted_submissions', 'is_quiz_assignment']

        for c in self.current_courses.keys():
            assignments = self.canvas.get_course(c).get_assignments()
            for assignment in assignments:
                a_dict = {}
                for x in assignment_attrs:
                    a_dict[x] = getattr(assignment, x, "")
                current_assignments[assignment.id] = a_dict

        return current_assignments

    def get_assignment_attrs(self):
        current_assignments = []

        for c in self.current_courses.keys():
            assignments = self.canvas.get_course(c).get_assignments()
            for assignment in assignments:
                print(getattr(assignment, "name", ""))
                print(getattr(assignment, "has_submitted_submissions", ""))

        # return current_assignments

    def cleanhtml(self, raw_html):
        # cleanr = re.compile('<.*?>')
        if (raw_html == None):
            return ""
        cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
        cleantext = re.sub(cleanr, '', raw_html)
        return cleantext

    def init_db(self):
        row = self.cv.collection.add_row()
        row.course = []

    def create_assignment(self, assignment):
        row = self.cv.collection.add_row()
        row.course = self.current_courses[assignment['course_id']]
        row.assignment_id = assignment['id']
        row.name = assignment['name']
        if (assignment['has_submitted_submissions']):
            row.status = "Done"
        else:
            row.status = "To Do"
        row.description = self.cleanhtml(assignment['description'])
        row.due_at_date = assignment['due_at_date'].astimezone(
            timezone('US/Eastern'))
        row.html_url = assignment['html_url']
        if (assignment['is_quiz_assignment']):
            row.assignment_type = "Quiz"
        else:
            row.assignment_type = "Uncategorized"

    def execute_query(self):
        result = self.cv.default_query().execute()
        return result

    def get_collection(self):
        return self.cv.collection.get_rows()

    def get_existing_assignment_ids(self):
        blocks = self.get_collection()
        return list(map(lambda x: x['assignment_id'], blocks))

    def get_active_courses(self):
        return self.courses
