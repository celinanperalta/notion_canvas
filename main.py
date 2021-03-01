from AssignmentDB import AssignmentDB
from datetime import datetime


def main():

    my_db = AssignmentDB()

    # assignments = my_db.get_current_assignments()

    # # print(assignments[6])

    # assignment_ids = list(assignments)

    # for i in range(0, len(assignments)):
    #     my_db.createAssignment(assignments.get(assignment_ids[i]))

    # result = my_db.executeQuery()
    # print("Added " + str(len(result)) + " rows.")

    blocks = my_db.get_collection()

    # for x in blocks:
    courses = my_db.get_active_courses()

    for x in courses:
        print(x)

    return 0


if __name__ == "__main__":
    main()
