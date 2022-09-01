from canvasapi import Canvas
from Assignment import Assignment
import config as config
import re
import NotionDB

class AssignmentDB:
    def __init__(self):
        self.canvas = Canvas(config.CANVAS_API_URL, config.CANVAS_API_KEY)
        self.user = self.canvas.get_user(config.CANVAS_USER_ID)
        self.current_courses = self.__get_current_courses()
        self.assignment_list = self.get_current_assignments()
        self.client = NotionDB.client
        self.cv = NotionDB.notion_db

    def __get_current_courses(self):
        current_classes = {}
        # lol @ this logic
        courses = list(filter(lambda x: config.CANVAS_TERM_NAME in x.name or x.name in config.CANVAS_TERM_NAME, self.user.get_courses(enrollment_state='active')))
        for course in courses:
            current_classes[course.id] = course
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

    def __print_assignment_attrs(self):
        for c in self.current_courses.keys():
            assignments = self.canvas.get_course(c).get_assignments()
            for assignment in assignments:
                print(getattr(assignment, "name", ""))
                print(getattr(assignment, "has_submitted_submissions", ""))

    def create_assignment(self, assignment):
        course = self.current_courses[assignment['course_id']]
        row = Assignment(assignment, course.name)
        props, children = row.create_notion_page()
        self.client.pages.create(parent={"database_id":config.NOTION_LINK}, properties = props, children = children)

    def get_active_courses(self):
        return self.current_courses

        
