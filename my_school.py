'''Anh (Fiona) Le
    S3999450
    Highest Level Attempted: HD Level
    Bugs/issues: 
    I had a fully functioning complete program with every method under the records class. I have refactored the whole program and brought half of the methods 
    away from the Records class to encapsulate them appropriately. However, there are still a few methods I was unable to push away from the Records class.'''

import sys
import os
import datetime

class IDError(Exception):
    '''Handles invalid course and student ID's'''
    pass

class CourseStudentNameError(Exception):
    '''Handles invalid course and student name inputs'''
    pass

class CourseStudentTypeError(Exception):
    '''Ensures only valid course type inputs, "C" for core and "E" for elective'''
    pass

class StudentModeError(Exception):
    '''Ensure only valid study mode inputs'''
    pass

class CreditPointError(Exception):
    '''Handles invalid credit point inputs (blank, non-numerical)'''
    pass

class SemesterError(Exception):
    '''handles invalid semester inputs'''
    pass

class GradeError(Exception):
    '''Handles invalid grade changes, i.e. blank and non-numerical values'''
    pass

class ResultEmptyError(Exception):
    '''Program quits gracefully in the event of an empty results file'''
    pass

class Results:
    def __init__(self, student, course, grade=""): 
        self.__student = student
        self.__course = course
        self.__grade = grade

    @property
    def student(self):
        return self.__student
    
    @property
    def course(self):
        return self.__course
    
    @property    
    def grade(self):
        return self.__grade
    
    @grade.setter
    def grade(self, grade):
        if not isinstance(grade, (int, float)):
            raise GradeError("Grade must be a numerical value!")
        elif grade < 0 or grade > 100:
            raise GradeError("Grade must be a valid number from 0 to 100!")
        self.__grade = grade

    def get_pass_rate(self, results_list):
        passing_count = 0
        total_grades = 0
        for result in results_list:
            if result.grade != "" and result.grade is not None:
                if float(result.grade) >= 49.5:
                    passing_count += 1
                total_grades += 1
        pass_rate = (passing_count / total_grades) * 100
        sys.stdout.write(f"\nPass Rate: {pass_rate:.2f}%.\n") #[3]
        return round(pass_rate, 2) #[4] rounding to 2 digits
    
    def get_course_summary(self, course_id, results_list):
        nfinish = 0
        nongoing = 0
        scores = []
        unique_students = set()  # [5] I used set to remove duplicate nfinish and nongoing counts
        for result in results_list:
            if result.course == course_id:
                if result.grade != "" and result.grade is not None:
                    if result.student not in unique_students:
                        scores.append(float(result.grade))
                        nfinish += 1
                        unique_students.add(result.student)
                else:
                    if result.student not in unique_students:
                        nongoing += 1
                        unique_students.add(result.student)
        if scores:
            average_score = sum(scores) / len(scores)
        else:
            average_score = None
        return nfinish, nongoing, round(average_score, 2)
    
class Course:
    def __init__(self, id, type, name, credit_point):
        self.__id = id #assumes names inputs are always valid (no numbers or special characters)
        self.__type = type
        self.__name = name
        self.__credit_point = credit_point

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, id):
        '''assumes the only valid format is a 7 character format with first 4 characters being letters "COSC"/"ISYS"/"MATH" 
        and last 3 characters being digits, e.g. COSC123. I implemented this on top of the HD level specs to account for a more comprehensive design approach.'''
        if id is None:
            raise IDError("Course ID cannot be blank!")
        elif len(id) != 7:
            raise IDError("Course ID must be 7 characters long!")
        elif not (str(id).startswith("COSC") or str(id).startswith("ISYS") or str(id).startswith("MATH")):
            raise IDError("Course ID must start with 'COSC,' 'ISYS,' or 'MATH'!")
        elif not str(id[4:]).isdigit(): 
            raise IDError("Last three characters must be digits!")
        self.__id = id

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, type):
        '''Ensures course types must be valid'''
        if type is None:
            raise CourseStudentTypeError("Course type cannot be blank!")
        elif str(type).upper() not in("C", "E"):
            raise CourseStudentTypeError("Course type must be either C(Core) or E(Elective)!")
        self.__type = type
    
    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, name):
        '''Ensures course names aren't empty and assumes course names don't have digits'''
        if name is None:
            raise CourseStudentNameError("Name cannot be blank!")
        self.__name = name

    @property
    def credit_point(self):
        return self.__credit_point

    @credit_point.setter
    def credit_point(self, credit_point):
        '''Ensures credit points are not null and is a digit, assumes credit point is not a negative integer or other weird number'''
        if credit_point is None:
            raise CreditPointError("Credit point cannot be blank!")
        elif not isinstance(credit_point, (int, float)): #ref
            raise CreditPointError("Credit point must be a numerical value!")
        self.__credit_point = credit_point

    def get_course_numbers(self, course_list):
        total_courses = len(course_list)
        sys.stdout.write(f"Total Courses: {total_courses}. ")

    def get_credit_points(self, course_id, course_list):
        for course in course_list:
            if course.id == course_id:
                return course.credit_point
        return None

class CoreCourse(Course):
    def __init__(self, id, type, name, credit_point):
        super().__init__(id, type, name, credit_point)

class ElectiveCourse(Course):
    def __init__(self, id, type, name, credit_point=None, semester=None):
        if credit_point is None:
            credit_point = 6
        super().__init__(id, type, name, credit_point)
        self.__semester = semester
    
    @property
    def semester(self):
        return self.__semester
    
    @semester.setter
    def semester(self, semester):
        '''Assumes the correct format for semester is "SemX" where "X" is a valid digit'''
        if semester is None:
            raise SemesterError("Semester cannot be blank!")
        elif len(semester) != 4:
            raise SemesterError("Semester must be 4 characters long!")
        elif str(semester[:3]).lower() != "Sem":
            raise SemesterError("Semester must start with 'Sem'!")
        elif not semester[3:].isdigit():
            raise SemesterError("Last character must be a digit!")
        self.__semester = semester
    
class Student:
    def __init__(self, id, name, type):
        self.__id = id #assumes names inputs are always valid (no numbers or special characters)
        self.__name = name
        self.__type = type

    @property
    def id(self):
        return self.__id
    
    @id.setter
    def id(self, id):
        '''Assumes student ids must follow the format "SXXX" where "X" is a valid digit. Assumes no need for more than 999 student ID's at this stage'''
        if id is None:
            raise IDError("Student ID cannot be blank!")
        elif len(id) != 4:
            raise IDError("Student ID must be 4 characters long!")
        elif not (str(id[0]).upper() == "S") or not isinstance(id[1:], int):
            raise IDError("Student ID must start with 'S' and end in 3 digits, e.g. 'S123'!")
        self.__id = id

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        if name is None:
            raise CourseStudentNameError("Name cannot be blank!")
        self.__name = name

    @property
    def type(self):
        return self.__type
    
    @type.setter
    def type(self, type):
        '''Assumes the only valid student types are undergraduate and postgraduate'''
        if type is None:
            raise CourseStudentTypeError("Student type cannot be blank!")
        elif str(type).upper() not in("UG", "PG"):
            raise CourseStudentTypeError("Student must be either UG(Undergrad) or PG(Postgrad)!")
        self.__type = type

    def get_student_numbers(self, student_list):
        total_students = len(student_list)
        sys.stdout.write(f"Total Students: {total_students}. ")

    def get_enrolment(self, student_id, results_list):
        nfinish = 0
        nongoing = 0
        unique_courses = set() #[5]
        for result in results_list:
            if result.student == student_id:
                if result.grade != "" and result.grade is not None:
                    if result.course not in unique_courses:
                        nfinish += 1
                        unique_courses.add(result.course)
                else:
                    if result.course not in unique_courses:
                        nongoing += 1
                        unique_courses.add(result.course)
        return nfinish, nongoing
    
    def get_gpa_100(self, student_id, results_list):
        grades = []
        for result in results_list:
            if result.student == student_id:
                if result.grade != "" and result.grade is not None:
                    grades.append(result.grade)
        if grades:
            gpa_100 = sum(grades) / len(grades)
        else:
            gpa_100 = None
        return round(gpa_100, 2)
    
    def get_gpa_4(self, student_id, results_list):
        grades = []
        for result in results_list:
            if result.student == student_id:
                if result.grade != "" and result.grade is not None:
                    grades.append(result.grade)
        if not grades:
            return 0.00, []
        total_points = 0.0
        gpa_points = []  
        for grade in grades:
            if grade < 49.5:
                gpa_points.append(0.00)
                total_points += 0.00
            elif 49.5 <= grade < 59.5:
                gpa_points.append(1.00)
                total_points += 1.00
            elif 59.5 <= grade < 69.5:
                gpa_points.append(2.00)
                total_points += 2.00
            elif 69.5 <= grade < 79.5:
                gpa_points.append(3.00)
                total_points += 3.00
            elif grade >= 79.5:
                gpa_points.append(4.00)
                total_points += 4.00
        gpa_4 = total_points / len(grades)
        return round(gpa_4, 2), gpa_points

class UGStudent(Student):
    mode = "FT"
    def __init__(self, id, name, type):
        super().__init__(id, name, type)
    
    @classmethod #[1]
    def set_mode(cls, mode):
        cls.mode = mode

    @classmethod #[1]
    def get_mode(cls):
        return cls.mode

class PGStudent(Student):
    def __init__(self, id, name, type, mode):
        super().__init__(id, name, type)
        self.__mode = mode

    @property
    def mode(self):
        return self.__mode
    
    @mode.setter
    def mode(self, mode):
        if mode is None:
            raise StudentModeError("Mode cannot be blank!")
        elif str(mode).upper() not in ("FT", "PT"):
            raise StudentModeError("Mode must be either FT (full-time) or PT (part-time)!")
        self.__mode = mode

class Records:
    student_obj = Student
    course_obj = Course
    results_obj = Results
    course_list = []
    student_list = []
    results_list = []
    
    def read_courses(self, course_file):
        with open(course_file, "r") as file:
            line = file.readlines()
            for l in line:
                fields = l.strip().split(",")
                course_id = fields[0].strip()
                if not (course_id.startswith("COSC") or course_id.startswith("ISYS") or course_id.startswith("MATH")):
                    raise IDError("All course ID's in the course file must start with 'COSC,' 'ISYS,' or 'MATH'!\n")
                course_type = fields[1].strip()
                course_name = fields[2].strip()
                if course_type.upper() == "C":
                    course_credit_points = int(fields[3])
                    course = CoreCourse(course_id, course_type, course_name, course_credit_points)
                    self.course_list.append(course)
                elif course_type.upper() == "E":
                    course_credit_points = int(fields[3])
                    course_semester = fields[4]
                    course = ElectiveCourse(course_id, course_type, course_name, course_credit_points, course_semester)
                    self.course_list.append(course)   

    def read_students(self, student_file):
        with open(student_file, "r") as file:
            line = file.readlines()
            for l in line:
                fields = l.strip().split(",")
                student_id = fields[0].strip()
                if not student_id.startswith("S"):
                    raise IDError("All student ID's in the student file must start with 'S'!\n")
                student_name = fields[1].strip()
                student_type = fields[2].strip()
                if student_type.upper() == "UG":
                    student = UGStudent(student_id, student_name, student_type)
                    self.student_list.append(student)
                elif student_type.upper() == "PG":
                    student_mode = fields[3].strip()
                    student = PGStudent(student_id, student_name, student_type, student_mode)
                    self.student_list.append(student)

    def read_results(self, result_file):
        with open(result_file, "r") as file:
            line = file.readlines()
            if not line:
                raise ResultEmptyError("The result file is empty!\n")
            for l in line:
                fields = l.strip().split(",")
                student_id = fields[0].strip()
                course_id = fields[1].strip()
                if len(fields) == 3:
                    grade = fields[2]
                    if grade != "":
                        try:
                            grade = float(grade)
                        except ValueError:
                            raise GradeError("Grade must be a numerical value!\n")
                        if grade < 0 or grade > 100:
                            raise GradeError("Grade must be within the valid range from 0 to 100!\n")
                result = Results(student_id.strip(), course_id.strip(), grade)
                self.results_list.append(result)

    def display_results(self):
        sys.stdout.write("\n\n- RESULTS -\n")
        sys.stdout.write("-" * (8 + (16 * len(self.course_list))) + "\n")
        sys.stdout.write("Student ID\t" + "\t\t".join(course.id for course in self.course_list) + "\n") #[2]
        sys.stdout.write("-" * (8 + (16 * len(self.course_list))) + "\n")
        for student in self.student_list:
            sys.stdout.write(f"{student.id:<10}")
            for course in self.course_list:
                result = None
                for r in self.results_list:
                    if r.student == student.id and r.course == course.id:
                        result = r.grade
                        if result == "":
                            result = "--"
                        break
                if result is None:
                    sys.stdout.write("".rjust(17))
                else:
                    sys.stdout.write(f"\t{result:>8}")
            sys.stdout.write("\n")
        sys.stdout.write("\nRESULTS SUMMARY\n\n")
        self.student_obj.get_student_numbers(self, self.student_list)
        self.course_obj.get_course_numbers(self, self.course_list)
        self.results_obj.get_pass_rate(self, self.results_list)
    
    def display_courses(self):
        sys.stdout.write("\n\n- COURSE INFORMATION -\n\n")
        sys.stdout.write("CORE COURSES\n")
        sys.stdout.write("-" * 128 + "\n")
        sys.stdout.write("{:<10}\t{:<20}\t{:<10}\t{:<10}\t{:<10}\t{:<10}\t{:<10}\t{:<10}\n".format(
            "CourseID", "Name", "Type", "Credit", "Semester", "Average", "Nfinish", "Nongoing"))
        sys.stdout.write("-" * 128 + "\n")
        core_courses = [course for course in self.course_list if course.type == "C"] 
        core_courses.sort(key=lambda course: self.results_obj.get_course_summary(self, course.id, self.results_list)[2], reverse=True) #[6]
        for course in core_courses:
            course_semester = "All"
            nfinish, nongoing, average_score = self.results_obj.get_course_summary(self, course.id, self.results_list)
            sys.stdout.write("{:<10}\t{:<20}\t{:>4}\t{:>14}\t{:>16}\t{:>7.2f}\t{:>15}\t{:>16}\n".format(
                course.id, course.name, course.type, course.credit_point, course_semester, average_score, nfinish, nongoing))
        sys.stdout.write("\n")
        sys.stdout.write("ELECTIVE COURSES\n")
        sys.stdout.write("-" * 128 + "\n")
        sys.stdout.write("{:<10}\t{:<20}\t{:<10}\t{:<10}\t{:<10}\t{:<10}\t{:<10}\t{:<10}\n".format(
                "CourseID", "Name", "Type", "Credit", "Semester", "Average", "Nfinish", "Nongoing"))
        sys.stdout.write("-" * 128 + "\n")
        elective_courses = [course for course in self.course_list if course.type == "E"] 
        elective_courses.sort(key=lambda course: self.results_obj.get_course_summary(self, course.id, self.results_list)[2], reverse=True) #[6]
        for course in elective_courses:
            nfinish, nongoing, average_score = self.results_obj.get_course_summary(self, course.id, self.results_list)
            sys.stdout.write("{:<10}\t{:<20}\t{:>4}\t{:>14}\t{:>16}\t{:>7.2f}\t{:>15}\t{:>16}\n".format(
                course.id, course.name, course.type, course.credit_point, course.semester, average_score, nfinish, nongoing))
        sys.stdout.write("\nCOURSE SUMMARY\n")
        self.get_hardest_core_course()
        self.get_hardest_elective_course()

    def get_hardest_core_course(self):
        core_courses = []
        lowest_average_score = min([self.results_obj.get_course_summary(self, course.id, self.results_list)[2] for course in self.course_list if course.type == "C"])
        for course in self.course_list:
            if course.type == "C" and self.results_obj.get_course_summary(self, course.id, self.results_list)[2] == lowest_average_score:
                core_courses.append(course)
        sys.stdout.write("\n")
        sys.stdout.write("Hardest Core Courses(s):\n")
        for course in core_courses:
            sys.stdout.write(f"{course.id} ({course.name}), Average score: {lowest_average_score}.\n")

    def get_hardest_elective_course(self):
        elective_courses = []
        lowest_average_score = min([self.results_obj.get_course_summary(self, course.id, self.results_list)[2] for course in self.course_list if course.type == "E"])
        for course in self.course_list:
            if course.type == "E" and self.results_obj.get_course_summary(self, course.id, self.results_list)[2] == lowest_average_score:
                elective_courses.append(course)
        sys.stdout.write("\n")
        sys.stdout.write("Hardest Elective Courses(s):\n")
        for course in elective_courses:
            sys.stdout.write(f"{course.id} ({course.name}), Average score: {lowest_average_score}.\n")

    def check_enrolment(self, student_id):
        '''Checks for minimum course enrolment requirements for each student type/mode, if student fails enrolment requirements, will append a "(!)" next to their name'''
        for student in self.student_list:
            if student.id == student_id:
                nfinish, nongoing = self.student_obj.get_enrolment(self, student_id, self.results_list)
                total_courses = nfinish + nongoing
                failed_enrolment = False  # Flag variable to track if enrolment requirements failed
                if student.type == "UG":
                    if total_courses < 4:
                        failed_enrolment = True
                elif student.type == "PG":
                    if student.mode == "FT":
                        if total_courses < 4:
                            failed_enrolment = True
                    elif student.mode == "PT":
                        if total_courses < 2:
                            failed_enrolment = True
                if failed_enrolment:
                    if "(!)" not in student.name: #prevents double-appending (!)
                        student.name += " (!)"

    def get_wgpa(self, student_id):
        '''Retrieves credit points from get_credit_points to calculate corresponding gpa's'''
        total_credit_points = 0
        weighted_gpa = 0
        gpa_4, gpa_points = self.student_obj.get_gpa_4(self, student_id, self.results_list)
        credit_points = []
        for result in self.results_list:
            if result.student == student_id:
                if result.grade != "" and result.grade is not None:
                    cpt = self.course_obj.get_credit_points(self, result.course, self.course_list)
                    if cpt is not None:
                        credit_points.append(cpt)
        if len(credit_points) != len(gpa_points):
            return None
        for i in range(len(gpa_points)):
            gpa_point = gpa_points[i]
            credit_point = credit_points[i]
            weighted_gpa += gpa_point * credit_point
            total_credit_points += credit_point
        if total_credit_points == 0:
            return None
        wgpa = weighted_gpa/total_credit_points
        return round(wgpa, 2)
        
    def get_highest_UG_GPA(self):
        '''Displays all UG students with highest GPA in the event there is a tie'''
        ug_students = []
        highest_gpa = max([self.student_obj.get_gpa_4(self, student.id, self.results_list)[0] for student in self.student_list if student.type == "UG"])
        for student in self.student_list:
            if student.type == "UG" and self.student_obj.get_gpa_4(self, student.id, self.results_list)[0] == highest_gpa:
                ug_students.append(student)
        sys.stdout.write("\n")
        sys.stdout.write("Best UG student(s):\n")
        for student in ug_students:
            sys.stdout.write(f"{student.id} ({student.name}), GPA: {highest_gpa:.2f}.\n")

    def get_highest_PG_GPA(self):
        '''Displays all PG students with highest GPA in the event there is a tie'''
        pg_students = []
        highest_gpa = max([self.student_obj.get_gpa_4(self, student.id, self.results_list)[0] for student in self.student_list if student.type == "PG"])
        for student in self.student_list:
            if student.type == "PG" and self.student_obj.get_gpa_4(self, student.id, self.results_list)[0] == highest_gpa:
                pg_students.append(student)
        sys.stdout.write("\n")
        sys.stdout.write("Best PG student(s):\n")
        for student in pg_students:
            sys.stdout.write(f"{student.id} ({student.name}), GPA: {highest_gpa:.2f}.\n")       

    def display_students(self):
        sys.stdout.write("\n\n- STUDENT INFORMATION -\n\n")
        sys.stdout.write("UNDERGRADUATE STUDENTS\n")
        sys.stdout.write("-" * 136 + "\n")
        sys.stdout.write("{:<10}\t{:<15}\t{:<10}\t{:<10}\t{:<10}\t{:<10}\t{:<10}\t{:<10}\t{:<10}\n".format(
            "StudentID", "Name", "Type", "Mode", "GPA(100)", "GPA(4)", "WGPA(4)", "Nfinish", "Nongoing"))
        sys.stdout.write("-" * 136 + "\n")
        undergraduate_students = [student for student in self.student_list if student.type.upper() == "UG"] #[6]
        undergraduate_students.sort(key=lambda student: self.get_wgpa(student.id), reverse=True)
        for student in undergraduate_students:
            mode = "FT"
            gpa_100 = self.student_obj.get_gpa_100(self, student.id, self.results_list)
            gpa_4, gpa_points = self.student_obj.get_gpa_4(self, student.id, self.results_list)
            wgpa = self.get_wgpa(student.id)
            nfinish, nongoing = self.student_obj.get_enrolment(self, student.id, self.results_list)
            self.check_enrolment(student.id)
            sys.stdout.write("{:<10}\t{:<15}\t{:>4}\t{:>12}\t{:>16.2f}\t{:>6.2f}\t{:>15.2f}\t{:>15}\t{:>16}\n".format(
                student.id, student.name, student.type, mode, gpa_100, gpa_4, wgpa, nfinish, nongoing))
        sys.stdout.write("\n")
        sys.stdout.write("POSTGRADUATE STUDENTS\n")
        sys.stdout.write("-" * 136 + "\n")
        sys.stdout.write("{:<10}\t{:<15}\t{:<10}\t{:<10}\t{:<10}\t{:<10}\t{:<10}\t{:<10}\t{:<10}\n".format(
            "StudentID", "Name", "Type", "Mode", "GPA(100)", "GPA(4)", "WGPA(4)", "Nfinish", "Nongoing"))
        sys.stdout.write("-" * 136 + "\n")
        postgraduate_students = [student for student in self.student_list if student.type.upper() == "PG"] #[6]
        postgraduate_students.sort(key=lambda student: self.get_wgpa(student.id), reverse=True)
        for student in postgraduate_students:
            gpa_100 = self.student_obj.get_gpa_100(self, student.id, self.results_list)
            gpa_4, gpa_points = self.student_obj.get_gpa_4(self, student.id, self.results_list)
            wgpa = self.get_wgpa(student.id)
            nfinish, nongoing = self.student_obj.get_enrolment(self, student.id, self.results_list)
            self.check_enrolment(student.id)
            sys.stdout.write("{:<10}\t{:<15}\t{:>4}\t{:>12}\t{:>16.2f}\t{:>6.2f}\t{:>15.2f}\t{:>15}\t{:>16}\n".format(
                student.id, student.name, student.type, student.mode, gpa_100, gpa_4, wgpa, nfinish, nongoing))
        sys.stdout.write("\nSTUDENT SUMMARY\n")
        self.get_highest_UG_GPA()
        self.get_highest_PG_GPA()

    def save_reports(self, report_file):
        timestamp = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S") #[7]
        with open(report_file, "a") as file:
            file.write("-"*88 + "\n")
            file.write(f"\nThis report was generated on: {timestamp}\n")
            sys.stdout = file  # Redirecting tables to report file [8]
            self.display_results()
            self.display_courses()
            self.display_students()
        sys.stdout = sys.__stdout__  

class Main:
    records = Records()
    def display_school_information(self):
        args = sys.argv
        args = ["my_school.py", "results.txt", "courses.txt", "students.txt"]
        if len(args) != 4:
            sys.stdout.write("Insufficient command line arguments.\nThe correct format is <result_file> <course_file> <student_file>.\n")
            sys.stdout.write("The program will be terminated.\n")
            return
        result_file = args[1]
        course_file = args[2]
        student_file = args[3]

        missing_files = []
        if not os.path.isfile(result_file): # [9]
            missing_files.append("'Results' file")
        if not os.path.isfile(course_file):
            missing_files.append("'Course' file")
        if not os.path.isfile(student_file):
            missing_files.append("'Student' file")
        if missing_files:
            sys.stdout.write("One or more required files do not exist:\n")
            for missing_file in missing_files:
                sys.stdout.write(f"\t- {missing_file} is missing.\n")
            sys.stdout.write("Please ensure these files exist in the same directory as the program.\nThe program will be terminated.\n\n")
            return
        try:
            self.records.read_results(result_file) 
        except ResultEmptyError as e:
            sys.stdout.write(str(e) + "The program will be terminated.\n")
            return
        except GradeError as e:
            sys.stdout.write(str(e) + "The program will be terminated.\n")
            return
        try:
            self.records.read_courses(course_file)
        except IDError as e:
            sys.stdout.write(str(e) + "The program will be terminated.\n")
            return
        try:
            self.records.read_students(student_file) 
        except IDError as e:
            sys.stdout.write(str(e) + "The program will be terminated.\n")
            return            
        self.records.display_results()
        self.records.display_courses()
        self.records.display_students()
        self.records.save_reports("reports.txt")

if __name__ == "__main__": # [10]
    main = Main()
    main.display_school_information()

'''Commentary
1. Originally I had placed conditions on the setters for student names to avoid any numbers or special characters. However I realised this prevented me in 
appending a "!" to students who did not enrol in the minimum number of courses required for their study mode. Took me a while to figure out the bug there ~
2. My course and student attributes nfinish and nogoing was counting duplicates which I was confused about, so I used sets to remove duplicate counts
3. Initially I had programmed the get_gpa_4 method to return only the averaged gpa_4 but that made it difficult to calulate wgpa. Hence I returned a list of grade points
for each course so I could calculated the weighted gpa more easily.
4. I repeated really long lines of code to save the displayed tables to a reports file. I found out a shorter implementation through redirecting the print function, referenced below.
5. When testing the report file, the (!) was appended twice to students who didn't meet the minimum enrolment requirments, so I added a condition to only append it for students who have not had the warning sign (!) already
appended to their names.
6. While it functioned perfectly, I initially finished this program with every single method that wasn't a getter or setter method within the Records class (and none in the appropriate classes). 
This caused my class diagram to look shabby with no methods under class Student, Course nor Results. I have done a major refactorisation to encapsulate some methods
under the appropriate classes and increase code modularity, but have faced some limitations for methods that call another method from another class. For example, in Class Records, the method get_hardest_core_course
calls the method get_course_summary from class Results. 
7. I initially had a fully complete program with only classes Student, PGStudent, Course and ElectiveCourse. Class Student essentially implied it was a UG student, and
class Course implied it was a core couse. I received feedback to distinguish course and student types using inheritance to improve my code which I have now implemented 
as: class Student, UGStudent(Student), PGStudent(Student), Course, CoreCourse(Course) and ElectiveCourse(Course).
'''

#References
# [1] Vishal. "Python Class Method Explained With Examples" PYNative.com. https://pynative.com/python-class-method/ (accessed Jun. 5, 2023) 
# [2] W3Schools. "Python String join() Method" W3Schools.com. https://www.w3schools.com/python/ref_string_join.asp (accessed May. 15, 2023)
# [3] I.V. Abba. "%.2f in Python – What does it Mean?" freeCodeCamp.org. https://www.freecodecamp.org/news/2f-in-python-what-does-it-mean/#:~:text=In%20Python%2C%20there%20are%20various,point%20number%20is%20rounded%20up. (accessed Jun. 5, 2023)
# [4] Programiz. "Python round()" Programiz.com. https://www.programiz.com/python-programming/methods/built-in/round (accessed May. 21, 2023)
# [5] manjeet_04. "Python – Ways to remove duplicates from list" GeeksForGeeks.org. https://www.geeksforgeeks.org/python-ways-to-remove-duplicates-from-list/ (accessed Jun. 6, 2023)
# [6] Programiz. "Python List sort()" Programiz.com. https://www.programiz.com/python-programming/methods/list/sort (accessed Jun. 8, 2023)
# [7] Vishal. "Python DateTime Format Using Strftime()" PYNative.com. https://pynative.com/python-datetime-format-strftime/ (accessed Jun. 9, 2023)
# [8] J. Kitchin. "Redirecting the print function" KitchinGroup.com. https://kitchingroup.cheme.cmu.edu/blog/2013/05/19/Redirecting-the-print-function/ (accessed Jun. 8, 2023)
# [9] Ihritik. "Python | os.path.isfile() method" GeeksforGeeks.com. https://www.geeksforgeeks.org/python-os-path-isfile-method/ (accessed May, 31, 2023)
# [10] Mike. "Python 101: Redirecting stdout" MouseVsPython.com. https://www.blog.pythonlibrary.org/2016/06/16/python-101-redirecting-stdout/ (accessed Jun. 5, 2023)