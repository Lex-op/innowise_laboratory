def main_menu() -> None:
    """Display the main menu options for Student Grade Analyzer."""
    print("--- Student Grade Analyzer ---")
    print("1. Add a new student")
    print("2. Add a grades for a student")
    print("3. Show report (all students)")
    print("4. Find top performer")
    print("5. Exit")


def student_exist(students: list, name: str) -> bool:
    """Check if a student with given name exists in the list (case-insensitive)."""
    for student in students:
        if student["name"].lower() == name.lower():
            return True
    return False


def add_student(students: list) -> None:
    """Add a new student to the system if they don't already exist."""
    name = input("Enter student name: ").strip()

    if not name:
        print("Student name cannot be empty")
        return
    
    if student_exist(students, name):
        print("Student already exists")
    else:
        students.append({"name": name, "grades": list()})


def add_grade_student(students: list) -> None:
    """Add grades for an existing student with comprehensive input validation.
    
    This function implements the grade addition feature for the Student Grade Analyzer.
    
    Args:
        students: List of student dictionaries with 'name' and 'grades' keys.
        
    Raises:
        ValueError: When grade input cannot be converted to integer.
        KeyboardInterrupt: When user interrupts grade input process.
        
    Note:
        Grades must be integers in the range [0, 100].
        Input 'done' or 'DONE' exits the grade entry loop.
        Student search is case-insensitive.
    """
    student_name = input("Enter a student name: ").strip()

    if not student_name:
            print("Student name cannot be empty")
            return
    
    if not student_exist(students, student_name):
        print("Student does not exists")
        return
    
    student = None 
    for key in students:
        if key["name"].lower() == student_name.lower():
            student = key

    while True:
        try:
            grade_input = input("Enter a grade (or 'done' to finish): ").strip().lower()
            if grade_input == 'done':
                break

            grade = int(grade_input)
            if grade < 0 or grade > 100:
                raise Exception("Grade must be between 0 and 100")

            student["grades"].append(grade)

        except ValueError:
            print("Invalid input, please enter number or 'done' to finish")
        except KeyboardInterrupt:
            print("Grade input cancelled")
            break  
        except Exception as e:
            print(e)    


def show_report(students: list) -> None:
    """Display comprehensive report of all students' grades and statistics."""
    sudents_averages = []
    print("--- Student Report ---")

    if not students:
        print("No students available.")
        return
    
    for student in students:
        if student["grades"]:
            avg = sum(student["grades"]) / len(student["grades"])
            sudents_averages.append(avg)
            print(f"{student['name']} average grade is {avg:.1f}") 
        else:
            print(f"{student['name']} average grade is N/A")    

    print("-" * 26)  
    
    if not sudents_averages:
        print("No grades to analyse")
        return
    else:
        print(f"Max Average: {max(sudents_averages):.1f}")
        print(f"Min Average: {min(sudents_averages):.1f}")
        print(f"Overall Average: {sum(sudents_averages) / len(sudents_averages):.1f}")


def find_top_performer(students: list) -> None:
     """Find and display the student with the highest average grade."""
     top_student: dict = {}
     try:
        top_student = max(students, key=lambda student: sum(student["grades"]) / len(student["grades"]))
        avg = sum(top_student["grades"]) / len(top_student["grades"])
        print(f"The student with the highest average is {top_student['name']} with a grade of {avg:.1f}")
     except ZeroDivisionError:
        print("No students with grades avalible")
     except ValueError:
        print("No valid students found")
     except KeyError as e:
        print(f"Missing data field - {e}")
     except Exception as e:
        print(f"Unexpected error: {e}")
            

def main() -> None:
    """Main program loop for Student Grade Analyzer application."""
    students: list = []

    while True:
        main_menu()

        try:
            choice = input()
        except KeyboardInterrupt:
            print("Program interrupted by user")
            break

        if choice == "1":
            add_student(students)

        elif choice == "2":
            add_grade_student(students)

        elif choice == "3":
            show_report(students)

        elif choice == "4":
            find_top_performer(students)

        elif choice == "5": 
            print("Exiting program.") 
            break      

        else:
            print("Invalid input, you should enter a number (1-5), try again")    


if __name__ == "__main__":
    main()          