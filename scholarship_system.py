from datetime import datetime

# SCHOLARSHIP ELIGIBILITY SCREENING SYSTEM
# Rule-based academic project. Uses only Python standard library.

MIN_CGPA = 7.00
MIN_ATTENDANCE = 75
MAX_INCOME = 500000
MAX_BACKLOGS = 1

MANDATORY_RULES = (
    "Academic", "Attendance", "Income", "Backlog", "Enrollment"
)

# Sample student records (fictional data for project demonstration).
students = [
    {
        "id": "BUC24011", "name": "Arjun Sharma", "programme": "BCA",
        "semester": 4, "cgpa": 8.72, "attendance": 91,
        "income": 320000, "backlogs": 0, "category": "OBC",
        "extra": "Yes", "first_gen": "No", "disability": "No",
        "enrollment": "Active"
    },
    {
        "id": "BUC24012", "name": "Meera Das", "programme": "B.Com",
        "semester": 3, "cgpa": 7.65, "attendance": 84,
        "income": 450000, "backlogs": 1, "category": "General",
        "extra": "No", "first_gen": "Yes", "disability": "No",
        "enrollment": "Active"
    },
    {
        "id": "BUC24013", "name": "Kabir Roy", "programme": "BBA",
        "semester": 2, "cgpa": 6.88, "attendance": 80,
        "income": 280000, "backlogs": 0, "category": "SC",
        "extra": "Yes", "first_gen": "No", "disability": "No",
        "enrollment": "Active"
    },
    {
        "id": "BUC24014", "name": "Ananya Sen", "programme": "BCA",
        "semester": 4, "cgpa": 6.40, "attendance": 69,
        "income": 620000, "backlogs": 2, "category": "General",
        "extra": "No", "first_gen": "No", "disability": "Yes",
        "enrollment": "Active"
    }
]


def validate_student(student):
    """Check whether the application data is valid."""
    try:
        if not student["id"].strip() or not student["name"].strip():
            return False
        if not 0 <= float(student["cgpa"]) <= 10:
            return False
        if not 0 <= float(student["attendance"]) <= 100:
            return False
        if float(student["income"]) < 0 or int(student["backlogs"]) < 0:
            return False
        return True
    except (KeyError, TypeError, ValueError, AttributeError):
        return False


def check_academic_eligibility(student):
    return student["cgpa"] >= MIN_CGPA


def check_attendance_eligibility(student):
    return student["attendance"] >= MIN_ATTENDANCE


def check_income_eligibility(student):
    return student["income"] <= MAX_INCOME


def check_backlog_eligibility(student):
    return student["backlogs"] <= MAX_BACKLOGS


def check_enrollment(student):
    return student["enrollment"].strip().lower() == "active"


def calculate_score(student):
    """Project-defined score out of 100."""
    cgpa_points = student["cgpa"] * 4
    attendance_points = student["attendance"] * 0.25
    income_points = max(0, 15 * (1 - student["income"] / 500000))
    backlog_points = 10 if student["backlogs"] == 0 else (
        5 if student["backlogs"] == 1 else 0
    )

    extra_points = 0
    if student["cgpa"] >= 8.50:
        extra_points += 3
    if student["attendance"] >= 90:
        extra_points += 2
    if student["extra"].strip().lower() == "yes":
        extra_points += 2
    if (student["first_gen"].strip().lower() == "yes"
            or student["disability"].strip().lower() == "yes"):
        extra_points += 3

    score = (cgpa_points + attendance_points + income_points
             + backlog_points + extra_points)
    return round(min(score, 100), 2)


def calculate_eligibility(student):
    """Check mandatory rules and return the final classification."""
    checks = {
        "Academic": check_academic_eligibility(student),
        "Attendance": check_attendance_eligibility(student),
        "Income": check_income_eligibility(student),
        "Backlog": check_backlog_eligibility(student),
        "Enrollment": check_enrollment(student)
    }

    all_mandatory = all(checks.values())

    if all_mandatory and student["cgpa"] >= 8.50 and student["attendance"] >= 85:
        status = "Highly Eligible"
    elif all_mandatory:
        status = "Eligible"
    elif (not checks["Academic"]
          and 6.75 <= student["cgpa"] < 7.00
          and checks["Attendance"] and checks["Income"]
          and checks["Backlog"] and checks["Enrollment"]):
        status = "Conditionally Eligible"
    else:
        status = "Not Eligible"

    return status, checks


def generate_explanation(student):
    status, checks = calculate_eligibility(student)
    messages = []

    for rule in MANDATORY_RULES:
        messages.append(
            rule + " requirement: " + ("PASS" if checks[rule] else "FAIL")
        )

    if status == "Highly Eligible":
        messages.append("Meets all mandatory rules and high-merit conditions.")
    elif status == "Eligible":
        messages.append("Meets all mandatory scholarship conditions.")
    elif status == "Conditionally Eligible":
        messages.append(
            "CGPA is between 6.75 and 6.99; all other mandatory rules pass."
        )
    else:
        messages.append(
            "One or more critical mandatory conditions are not satisfied."
        )

    if student["extra"].strip().lower() == "yes":
        messages.append("Additional consideration: extracurricular achievement.")
    if (student["first_gen"].strip().lower() == "yes"
            or student["disability"].strip().lower() == "yes"):
        messages.append("Additional consideration: special consideration.")

    return messages


def display_students():
    print("\nSTUDENT APPLICATIONS")
    print("-" * 88)
    for s in students:
        print(f'{s["id"]} | {s["name"]} | {s["programme"]} | '
              f'CGPA: {s["cgpa"]} | Attendance: {s["attendance"]}%')
    print("-" * 88)


def screen_student(student):
    if not validate_student(student):
        print("Invalid student information.")
        return

    status, checks = calculate_eligibility(student)
    print("\nSTUDENT SCREENING RESULT")
    print("Student:", student["name"])
    print("Student ID:", student["id"])
    for rule in MANDATORY_RULES:
        print(rule + ":", "PASS" if checks[rule] else "FAIL")
    print("Eligibility:", status)
    print("Eligibility Score:", calculate_score(student), "/ 100")
    print("Explanation:")
    for message in generate_explanation(student):
        print("-", message)


def screen_all_students():
    for student in students:
        screen_student(student)


def search_student():
    student_id = input("Enter Student ID: ").strip().upper()
    for student in students:
        if student["id"].upper() == student_id:
            screen_student(student)
            return
    print("Student not found.")


def display_by_status(wanted_status):
    found = False
    for student in students:
        status, _ = calculate_eligibility(student)
        if status == wanted_status:
            print(student["id"], "-", student["name"],
                  "| Score:", calculate_score(student))
            found = True
    if not found:
        print("No students found in this category.")


def rank_eligible_students():
    eligible = []
    for student in students:
        status, _ = calculate_eligibility(student)
        if status != "Not Eligible":
            eligible.append(student)

    eligible.sort(key=lambda s: calculate_score(s), reverse=True)

    print("\nRANKING OF ELIGIBLE APPLICANTS")
    if not eligible:
        print("No eligible applicants.")
        return

    for rank, student in enumerate(eligible, start=1):
        status, _ = calculate_eligibility(student)
        print(f'{rank}. {student["name"]} ({student["id"]}) - '
              f'{status} - Score: {calculate_score(student)}')


def scholarship_summary():
    counts = {
        "Highly Eligible": 0,
        "Eligible": 0,
        "Conditionally Eligible": 0,
        "Not Eligible": 0
    }

    for student in students:
        status, _ = calculate_eligibility(student)
        counts[status] += 1

    print("\nSCHOLARSHIP SUMMARY")
    for status, count in counts.items():
        print(status + ":", count)
    print("Total applications:", len(students))


def generate_report():
    now = datetime.now()
    print("\n" + "=" * 58)
    print("CONSOLIDATED SCHOLARSHIP SCREENING REPORT")
    print("Date and Time:", now.strftime("%d-%m-%Y %I:%M:%S %p"))
    print("=" * 58)

    for student in students:
        status, _ = calculate_eligibility(student)
        print(f'{student["id"]} | {student["name"]} | {status} | '
              f'Score: {calculate_score(student)}')
    scholarship_summary()
    print("=" * 58)


def main():
    while True:
        print("\n==============================================")
        print(" SCHOLARSHIP ELIGIBILITY SCREENING SYSTEM")
        print("==============================================")
        print("1. Display All Applications")
        print("2. Screen Individual Student")
        print("3. Screen All Students")
        print("4. Search Student")
        print("5. Display Eligible Students")
        print("6. Display Highly Eligible Students")
        print("7. Rank Eligible Students")
        print("8. Display Scholarship Summary")
        print("9. Display Screening Date and Time")
        print("10. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            display_students()
        elif choice == "2":
            student_id = input("Enter Student ID: ").strip().upper()
            found = False
            for student in students:
                if student["id"].upper() == student_id:
                    screen_student(student)
                    found = True
                    break
            if not found:
                print("Student not found.")
        elif choice == "3":
            screen_all_students()
        elif choice == "4":
            search_student()
        elif choice == "5":
            print("\nELIGIBLE STUDENTS")
            display_by_status("Highly Eligible")
            display_by_status("Eligible")
            display_by_status("Conditionally Eligible")
        elif choice == "6":
            print("\nHIGHLY ELIGIBLE STUDENTS")
            display_by_status("Highly Eligible")
        elif choice == "7":
            rank_eligible_students()
        elif choice == "8":
            scholarship_summary()
        elif choice == "9":
            print("Screening Date and Time:",
                  datetime.now().strftime("%d-%m-%Y %I:%M:%S %p"))
        elif choice == "10":
            print("Thank you for using the Scholarship Screening System.")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 10.")


if __name__ == "__main__":
    main()
