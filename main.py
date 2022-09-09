from AssignmentDB import AssignmentDB
from datetime import datetime
import NotionDB as ndb

def run_canvas_to_notion():
    adb = AssignmentDB()

    assignments = adb.get_current_assignments()
    existing_assignments = ndb.get_existing_rows()

    assignment_ids = list(filter(lambda x: x not in existing_assignments, assignments))

    for i in range(0, len(assignment_ids)):
        print(f"Importing assignment {i+1}/{len(assignment_ids)}")
        adb.create_assignment(assignments.get(assignment_ids[i]))
    
    if (len(assignment_ids) == 0):
        print("Nothing new.")

    for i in range(0, len(existing_assignments)):
        try:
            if adb.update_assignment(existing_assignments[i], assignments.get(existing_assignments[i])) == 0:
                print(f"Updated: assignment {existing_assignments[i]}")
            else:
                print(f"Failed to update: assignment {existing_assignments[i]}")
        except:
            print(f"Failed to update: assignment {existing_assignments[i]}")

def main():

    run_canvas_to_notion()
        
    return 0


if __name__ == "__main__":
    main()
