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


def print_menu():
    print("\n==== University Course Prerequisite System ====")
    print("1. View All Course")
    print("2. View Course Details")
    print("3. View Prerequisites")
    print("4. View Courses Unlocked by a Course")
    print("5. Exit")


def display_courses(courses):
    print("Available courses")
    count = 0
    for course in courses.values():
        count += 1
        print(f"{count}. ", end="")
        course.display_course()


def view_course_details(courses):
    code = input("Enter course code: ").strip().upper()
    print(courses[code])


def view_prerequisites(courses, course_graph):
    code = input("Enter course code: ").strip().upper()
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
    pass


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

    choice = ""
    while choice != "5":
        print_menu()
        choice = input("Enter choice (1-5): ")

        if choice == "1":
            display_courses(courses)
        elif choice == "2":
            view_course_details(courses)
        elif choice == "3":
            view_prerequisites(courses, course_graph)
        elif choice == "4":
            view_unlocked_courses(courses, course_graph)
        elif choice == "5":
            print("Exiting Course Prerequisite System. Goodbye!")


if __name__ == "__main__":
    main()