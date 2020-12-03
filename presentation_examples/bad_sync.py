from threading import Thread

STUDENTS = []


def add_student_if_not_exists(name, points):
    if not any(s["name"] == name for s in STUDENTS):
        print("missing record in list")
        student = {"name": name, "points": 0}
        for _ in range(points):
            student["points"] += 1

        STUDENTS.append(student)


for _ in range(1000):
    Thread(target=add_student_if_not_exists, args=("bob", 250000)).start()

print(STUDENTS)
