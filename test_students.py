import os
import pytest
from main import (
    import_from_file,
    export_attendance,
    add_student,
    edit_student
)

TEST_FILE = "test_students.csv"

@pytest.fixture
def test_file():
    yield TEST_FILE
    if os.path.exists(TEST_FILE):
        os.remove(TEST_FILE)


# tests for saving to file and loading from file
def test_import_from_file(test_file):
    with open(TEST_FILE, "w") as f:
        f.write("John,Doe,yes\nJane,Smith,no\n")
    
    students = import_from_file(TEST_FILE)
    assert len(students) == 2
    assert students[0] == {"first_name": "John", "last_name": "Doe", "present": True}
    assert students[1] == {"first_name": "Jane", "last_name": "Smith", "present": False}

def test_export_attendance(test_file):
    students = [
        {"first_name": "Alice", "last_name": "Brown", "present": True},
        {"first_name": "Bob", "last_name": "Green", "present": False},
    ]
    
    export_attendance(students, TEST_FILE)
    with open(TEST_FILE, "r") as f:
        lines = f.readlines()
    assert lines == ["Alice,Brown,yes\n", "Bob,Green,no\n"]


# tests for operations on students and attendance
def test_add_student(test_file):
    if os.path.exists(TEST_FILE):
        os.remove(TEST_FILE)
    
    add_student("Charlie", "Johnson", TEST_FILE)
    
    with open(TEST_FILE, "r") as f:
        lines = f.readlines()
    assert lines[1].strip() == "Charlie,Johnson,False"


def test_edit_student(test_file):
    with open(TEST_FILE, "w") as f:
        f.write("first_name,last_name,present\nJohn,Doe,False\nJane,Smith,False\n")
    edit_student("John", "Doe", "Jonathan", "Doe", TEST_FILE)

    students = import_from_file(TEST_FILE)
    assert any(s["first_name"] == "Jonathan" and s["last_name"] == "Doe" for s in students)
    assert not any(s["first_name"] == "John" and s["last_name"] == "Doe" for s in students)

def test_import_from_file_empty_line(test_file):
    with open(test_file, "w") as f:
        f.write("John,Doe,yes\n\nJane,Smith,no\n") #adding students with one empty line between them
    
    students = import_from_file(test_file)
    assert len(students) == 2  #program should ignore the empty line in that case
    assert students[0] == {"first_name": "John", "last_name": "Doe", "present": True}

#trying to edit a student that doesnt exist
def test_edit_student_not_found(test_file):
    with open(test_file, "w") as f:
        f.write("first_name,last_name,present\nJohn,Doe,False\n")
    
    with pytest.raises(ValueError):
        edit_student("Jane", "Smith", "Janet", "Smith", test_file)

#trying to import things from a file that doesnt exist
def test_import_from_file_missing_file():
    with pytest.raises(FileNotFoundError):
        import_from_file("non_existent.csv")

#trying to add two students, the second one without lastname
def test_import_from_file_missing_fields(test_file):
    with open(test_file, "w") as f:
        f.write("John,Doe\nJane\n") 
    with pytest.raises(ValueError):
        import_from_file(test_file)
