from bakery import assert_equal
from drafter import *
from dataclasses import dataclass

hide_debug_information()
set_website_framed(False)

set_website_title("Assignment Tracker")
set_site_information(
    author = "Ashlyn Almeida (aalmeida@udel.edu) and Emily Bosak (erbosak@udel.edu)",
    description = """ This website acts as an assignment tracker.
    Users can add as many courses as they'd like,
    add assignments for each course,
    and calculate an average grade based on each
    assignment grade for that course. """,
    sources = [""],
    planning = [""],
    links = [""]
)

#-------------------background-------------------
add_website_css("""
body {
    background-color: lightpink;
    font-size: 20px;
}

.name-box {
    background-color: pink;
    float: right;
}
""")

#-----------------dataclasses------------------------

@dataclass
class Assignment:
    name: str
    description: str
    progress: str
    assignment_grade: float
    
@dataclass
class Course:
    name: str
    assignment_list: list[Assignment]
    course_grade: float
    
@dataclass
class State:
    user_name: str
    current_course: Course
    courses: list[Course]
    
#-----------------------routes-------------------------
    
@route
def index(state: State) -> Page:
    content = [
    Header("Course Tracker"),
    "Enter a Course:",
    TextBox("course_name", state.current_course.name),
    Button("Save Course", "/save_course"),
    Button("To Courses!", "/courses_list")
        ]
    return Page(state, content = content)

@route
def save_course(state: State, course_name: str) -> Page:
    current_course = Course(course_name, [], 0.0)
    state.courses.append(current_course)
    return index(state)

@route
def courses_list(state: State) -> Page:
    content = [Header("Courses List", 3)]
    list_of_courses = state.courses
    for course in list_of_courses:
            content.append(Button(course.name, "/course_page", arguments = Argument("course", course.name)))
    content.append(Button("Add Another Course", "/index"))
    return Page(state, content = content)

@route
def course_page(state: State, course: str) -> Page:
    for Course in state.courses:
        if Course.name == course:
            items = []
            for a in Course.assignment_list:
                assignment_text = "Name: " + a.name + " | Description: " + a.description + " | Progress: " + a.progress + " | Grade: " + str(a.assignment_grade) + "%"
                items.append(assignment_text)
            content = [
                Header(course),
                Header("Assignments:", 5),
                NumberedList(items),
                Header("Grade:", 5),
                Header((str(Course.course_grade) + "%"), 6),
                Button("Add Assignments", "/add_assignments", arguments = Argument("course", course)),
                Button("Return", "/courses_list")
                ]
            if not Course.assignment_list:
                content = [
                    Header(course),
                    Header("Assignments:", 5),
                    NumberedList(Course.assignment_list),
                    Header("Grade:", 5),
                    Header((str(Course.course_grade) + "%"), 6),
                    Button("Add Assignments", "/add_assignments", arguments = Argument("course", course)),
                    Button("Return", "/courses_list")
                    ]
            return Page(state, content = content)
    return Page(state, content = [Header("Course Not Found! Please Reload the Page and Try Again.", 5)])

@route
def average_assignment_grade(state: State, course: str) -> Page:
    for Course in state.courses:
        if Course.name == course:
            sum_grade = 0
            count_grade = 0
            if Course.assignment_list:
                for a in Course.assignment_list:
                    sum_grade += a.assignment_grade
                    count_grade += 1
                average = sum_grade/count_grade
                Course.course_grade = average
                return course_page(state, course)
            else:
                Course.course_grade = 0.0
                return course_page(state, course)
            
@route
def add_assignments(state: State, course: str) -> Page:
    blank_assignment = Assignment("", "", "", 0.0)
    content = [
        "Enter Assignment Name:",
        TextBox("assignment_name", blank_assignment.name),
        "Enter Assignment Description:",
        TextBox("assignment_desc", blank_assignment.description),
        "Enter Progress (Not Started, In Progress, or Done):",
        TextBox("assignment_progress", blank_assignment.progress),
        "Enter Assignment Grade:",
        TextBox("assignment_grade", blank_assignment.assignment_grade),
        "Save Assignment Data:",
        Button("Save", "/save_assignment", arguments = Argument("course", course))
        ]
    return Page(state, content = content)

@route
def save_assignment(state: State, course: str, assignment_name: str, assignment_desc: str, assignment_progress: str, assignment_grade: str) -> Page:
    current_assignment = Assignment(
        assignment_name,
        assignment_desc, assignment_progress,
        float(assignment_grade)
    )
    for Course in state.courses:
        if Course.name == course:
            Course.assignment_list.append(current_assignment)
    return average_assignment_grade(state, course)


start_server(State("", Course("", [], 0.0), []))
