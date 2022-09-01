from AssignmentDB import AssignmentDB
from datetime import datetime
import NotionDB as ndb

def run_canvas_to_notion():
    adb = AssignmentDB()

    assignments = adb.get_current_assignments()
    existing_assignments = ndb.get_existing_rows()

    assignment_ids = list(filter(lambda x: x not in existing_assignments, assignments))

    for i in range(0, len(assignment_ids)):
        adb.create_assignment(assignments.get(assignment_ids[i]))

def main():

    run_canvas_to_notion()
        
    return 0


if __name__ == "__main__":
    main()
