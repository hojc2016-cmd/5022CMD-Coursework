class Graph:
    def __init__(self):
        self.graph = {}

    def addVertex(self, vertex):
        if vertex in self.graph:
            return False

        self.graph[vertex] = []
        return True

    def addEdge(self, vertex_start, vertex_end):
        if vertex_start not in self.graph or vertex_end not in self.graph:
            return False

        if vertex_end in self.graph[vertex_start]:
            return False

        self.graph[vertex_start].append(vertex_end)
        return True

    def listIncomingAdjacentVertex(self, vertex):
        if vertex not in self.graph:
            return None

        incoming = []

        for vertex_start, vertex_end in self.graph.items():
            if vertex in vertex_end:
                incoming.append(vertex_start)

        return incoming

class Course:
    def __init__(self, courseCode, courseName, creditHours, level):
        self.courseCode = courseCode
        self.courseName = courseName
        self.creditHours = creditHours
        self.level = level

    def __str__(self):
        return (
            f"Course Code: {self.courseCode}\n"
            f"Course Name: {self.courseName}\n"
            f"Credit Hours: {self.creditHours}\n"
            f"Level: {self.level}"
        )

    def display_course(self):
        print(f"{self.courseCode} - {self.courseName}")

def get_integer(prompt):
    value = None

    while value is None:
        try:
            value = int(input(prompt))
        except ValueError:
            print("Please enter a whole number.")

    return value

def get_text(prompt):
    value = input(prompt).strip()

    while not value:
        print("This field cannot be empty.")
        value = input(prompt).strip()

    return value

def get_course_code(prompt, courses):
    code = get_text(prompt).upper()

    while code not in courses:
        print("Course not found. Please enter an existing course code.")
        code = get_text(prompt).upper()

    return code

def print_menu():
    print("\n==== University Course Prerequisite System ====")
    print("1. View All Course")
    print("2. View Course Details")
    print("3. View Prerequisites")
    print("4. View Courses Unlocked by a Course")
    print("5. Exit")


def view_all_courses(courses):
    print("Available courses")
    count = 0
    for course in courses.values():
        count += 1
        print(f"{count}. ", end="")
        course.display_course()


def view_course_details(courses):
    code = get_course_code("Enter course code: ", courses)
    print(courses[code])


def view_prerequisites(courses, course_graph):
    code = get_course_code("Enter course code: ", courses)
    prerequisites = course_graph.listIncomingAdjacentVertex(code)

    if prerequisites is None:
        print("Course not found.")
    elif not prerequisites:
        print("This course has no prerequisites.")
    else:
        print(f"Prerequisites for {code} - {courses[code].courseName}:")
        for prerequisite_code in prerequisites:
            courses[prerequisite_code].display_course()


def view_unlocked_courses(courses, course_graph):
    code = get_course_code("Enter course code: ", courses)

    if code not in course_graph.graph:
        print("Course not found.")
        return

    unlocked_courses = course_graph.graph[code]

    if not unlocked_courses:
        print("This course unlocks no other courses.")
    else:
        print(f"Courses unlocked by {code} - {courses[code].courseName}:")
        for unlocked_code in unlocked_courses:
            courses[unlocked_code].display_course()


def main():
    courses = {
        "CS101": Course("CS101", "Programming Fundamentals", 3, "core"),
        "MA101": Course("MA101", "Discrete Mathematics", 3, "core"),
        "CS201": Course("CS201", "Data Structures", 3, "core"),
        "CS301": Course("CS301", "Advanced Algorithms", 3, "core"),
        "CS302": Course("CS302", "Software Engineering", 3, "elective")
    }

    course_graph = Graph()

    for course_code in courses:
        course_graph.addVertex(course_code)

    course_graph.addEdge("CS101", "CS201")
    course_graph.addEdge("MA101", "CS201")
    course_graph.addEdge("CS201", "CS301")
    course_graph.addEdge("CS201", "CS302")

    choice = 0
    while choice != 5:
        print_menu()
        choice = get_integer("Enter choice (1-5): ")

        while choice < 1 or choice > 5:
            print("Please choose a number from 1 to 5.")
            choice = get_integer("Enter choice (1-5): ")

        if choice == 1:
            view_all_courses(courses)
        elif choice == 2:
            view_course_details(courses)
        elif choice == 3:
            view_prerequisites(courses, course_graph)
        elif choice == 4:
            view_unlocked_courses(courses, course_graph)
        elif choice == 5:
            print("Exiting Course Prerequisite System. Goodbye!")


if __name__ == "__main__":
    main()