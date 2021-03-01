from canvasapi import Canvas
import config as config
from datetime import datetime

canvas = Canvas(config.CANVAS_API_URL, config.CANVAS_API_KEY)
user = canvas.get_user(config.CANVAS_USER_ID)
courses = user.get_courses()

# Get current classes

def get_current_courses():
    current_classes = {}
    for course in courses:
        if (hasattr(course, 'enrollment_term_id') and course.enrollment_term_id == config.CANVAS_ENROLLMENT_TERM):
            course_name = "".join(course.name[6:14].split())
            print(course_name + " " + str(course.id))
            current_classes[course.id] = course_name
    return current_classes

# Get current assignments given list of courses

def get_current_assignments(current_classes):
    current_assignments = {}
    assignment_attrs = ['name', 'description',
                        'due_at_date', 'course_id', 'id', 'html_url', 'locked_for_user']

    for c in current_classes.keys():
        assignments = canvas.get_course(c).get_assignments()
        for assignment in assignments:
            a_dict = {}
            for x in assignment_attrs:
                a_dict[x] = getattr(assignment, x, "")
            current_assignments[assignment.id] = a_dict

    return current_assignments





