class Graph:
    def __init__(self):
        self.graph = {}

    def addVertex(self):
        pass

    def addEdge(self):
        pass

    def listIncomingAdjacentVertex(self):
        pass

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
        pass

    def course_details(self):
        pass

    def prerequisite_courses(self):
        pass

    def course_unlocked(self):
        pass

def main():
    course = Course("CS101", "Programming Fundamentals", 3, "core")
    print(course)


if __name__ == "__main__":
    main()