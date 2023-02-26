import numpy as np
import time
from datetime import datetime
import sys
import os
import statistics
import math

class Program: 
    def readData(): # This is the csv reader, it will read the data inside the csv file and will be used as basis for the program.
        data = np.loadtxt('studentDetails.csv', dtype=str, delimiter=',', skiprows=1)
        # for each_data in data:
        #     print(each_data)
        return data


    def startFeature():
        levels_chosen = [] # Storage of the levels chosen  
        # This is where the user will choose the level of the record he/she is looking for
        initial_student_level = input("What is your student level?\n[U]ndergraduate\n[G]raduate\n[B]oth? ") 
        if initial_student_level.upper() == "U": # If undergraduate array will store choice then will look for the record using getStudentID
            levels_chosen.append("U")
            Program.getStudentID(levels_chosen)
        elif initial_student_level.upper() == "G": # If graduate prompt asks what graduate level user is, if M or D or Both
            # Then array stores choice then will look for the studentID using the choice.
            secondary_student_level = input("Please specify graduate level.\n[M]aster\n[D]octorate\n[B0]th? ")
            if secondary_student_level.upper() == "M" or secondary_student_level.upper() == "B0":
                levels_chosen.append("M")
            if secondary_student_level.upper() == "D" or secondary_student_level.upper() == "B0":
                levels_chosen.append("D")
            Program.getStudentID(levels_chosen)

        elif initial_student_level.upper() == "B": # If both undergraduate and graduate, user's first choice (U) is stored then prompt
            # asks whether graduate level is M, D, or Both then 2nd choice is stored then studentID is looked for using the getStudentID.
            levels_chosen.append("U")
            secondary_student_level = input("Please specify graduate level.\n[M]aster\n[D]octorate\n[BO]th? ")
            if secondary_student_level.upper() == "M" or secondary_student_level.upper() == "BO":
                levels_chosen.append("M")
            if secondary_student_level.upper() == "D" or secondary_student_level.upper() == "BO":
                levels_chosen.append("D")
            Program.getStudentID(levels_chosen)



    def getStudentID(student_level): # Will look for the student ID based on your choice of student level in the beginning.
        try:
            transcript_records = Program.readData() # Stores the data on csv
            student_id = input("What is your student id? ") # Prompt gets the StudentID of user
            chosen_records = []
            for record in transcript_records: # Then the records in the csv will be the data used to look for user. 
                if "U" in student_level: # If they chose U, if it is BS & matches the student ID chosen_records will store the user's record
                    if "BS" in record[6] and student_id == record[1]:
                        chosen_records.append(record)
                if "M" in student_level or "D" in student_level: # On the event that they choose Masteral or Doctoral.
                    if "M" in record[6] and student_id == record[1]: # If it's masteral and ID matches, chosen_records will store the data
                        chosen_records.append(record) 
                    if "D" in record[6] and student_id == record[1]: # If it's doctoral and ID matches, chosen_records will store the data
                        chosen_records.append(record)
            if not chosen_records: # If data provided is not in saved records, error will be raised.
                raise ValueError()
            else:
                Program.menuFeature(chosen_records) # else. menu is launched.


        except ValueError: # If data provided is not in saved records, error will be raised.
            print("No corresponding records found.\n\n")
            Program.startFeature()

    def menuFeature(corresponding_records): # This will launch if all the data provided by the user matches the ones in record.
        print("Student Transcription Generation System")
        print("==================================================")
        print("1. Student details") # Provides student details, presented by the detailsFeature function.
        print("2. Statistics") # Provides student's stats, presented by the statisticsFeature function.
        print("3. Transcript Based on Major Courses") # Provides the minor transcript of subjects, presented by minorTranscriptFeature func.
        print("4. Transcript Based on Minor Courses") # Provides the major transcript of subjects, presented by majorTranscriptFeature func.
        print("5. Full Transcript") # Provides the students's full transcript of subjects, presented by  fullTranscriptFeature function
        print("6. Previous Transcript Requests") # Provides the history of transcript record requests from the student
        print("7. Select Another Student") # Allows choosing another student for transcript record findings.
        print("8. Terminate the System") # Exits the program
        print("==================================================")
        choice = int(input("Enter Your Feature: "))
        if choice == 1:
            Program.detailsFeature(corresponding_records)
        elif choice == 2:
            Program.statisticsFeature(corresponding_records)
        elif choice == 3:
            Program.majorTranscriptFeature(corresponding_records)
        


    def detailsFeature(current_records): # Present student details, prints them in format then stores them in a list.
        name = current_records[0][2]
        stdID = current_records[0][1]
        levels = ", ".join(record[5] for record in current_records) 
        term_numbers = ", ".join(record[9] for record in current_records)
        colleges = ", ".join(record[3] for record in current_records)
        departments =", ".join(record[4] for record in current_records)
        print(Program.printDetails(name, stdID, levels, term_numbers, colleges, departments))
        with open("std{}details.txt".format(stdID), "w") as file:
            file.write(Program.printDetails(name, stdID, levels, term_numbers, colleges, departments))
    
    def printDetails(name, stdID, levels, term_numbers, colleges, departments): # This will be the printing function used in studentDetails func
        # This is the format to which the details are presented.
        name_detail = f"Name: {name}"
        std_ID = f"stdID: {stdID}"
        level_detail = f"Level(s): {levels}"
        term_number_detail = f"Number Of Terms: {term_numbers}"
        college_detail = f"College(s): {colleges}"
        department_detail = f"Department(s): {departments}"
        return f"{name_detail}\n{std_ID}\n{level_detail}\n{term_number_detail}\n{college_detail}\n{department_detail}"

    def statisticsFeature(current_records): # Presents statistics about student's grades, average of those grades, and highest grade per term.
        current_id = current_records[0][1]
        # data = np.loadtxt('{}.csv'.format(current_id), dtype=str, delimiter=',', skiprows=1)
        data = np.loadtxt('201008000.csv', dtype=str, delimiter=',', skiprows=1)
        with open("std201008000statistics.txt", "w") as file: # Saves the data in the text specified.
            file.write(Program.printStatistics(current_records, data))


    def printStatistics(statistics_records, current_data):
        text_container = "" # Contains the data to be saved in the text based on the format presented by the str_container.
        for record in statistics_records:
            str_container = "" # Contains the format to which the data is to be presented.
            overall_average = 0 # Container for the overall average to be presented later.
            scores = [] # Stores the grades from the csv.
            max_term = 0 # Stores the max term recorded in the csv.
            is_repeating = False # Boolean whether student is a repeating or not.
            if "BS" in record[6]: # If student has BS as degree, he/she is labeled undergraduate and taking Bachelor of Science. 
                level = "Undergraduate"
                overall_average = 0
                courses = []
                for row in current_data:
                    if "BS" in row[1]:
                        scores.append(int(row[7])) 
                        if int(row[2]) > max_term: # Will check if the current term being checked is the highest term and will be stored as the max_term.
                            max_term = int(row[2])
                        if row[4] in courses: # If course already exists in the container, is_repeating condition is true.
                            is_repeating = True
                        courses.append(row[4])
                    print(courses)

            elif "M" in record[6]: # If student has M as degree, he/she is labeled graduate and taking Masteral degree.
                level = "Graduate(M)"
                overall_average = 0
                courses = []
                for row in current_data:
                    if "M" in row[1]:           
                        scores.append(int(row[7]))
                        if int(row[2]) > max_term:  # Will check if the current term being checked is the highest term and will be stored as the max_term.
                            max_term = int(row[2])
                        if row[4] in courses: # If course already exists in the container, is_repeating condition is true.
                            is_repeating = True
                        courses.append(row[4])

            elif "D" in record[6]: # If student has D as degree, he/she is labeled graduate and taking Doctoral degree.
                level = "Graduate(D)"
                overall_average = 0
                courses = []
                for row in current_data:
                    if "D" in row[1]:    
                        scores.append(int(row[7]))
                        if int(row[2]) > max_term:  # Will check if the current term being checked is the highest term and will be stored as the max_term.
                            max_term = int(row[2])
                        if row[4] in courses: # If course already exists in the container, is_repeating condition is true.
                            is_repeating = True
                        courses.append(row[4])

            overall_average = statistics.mean(scores) # Will calculate the overall average of the student's grades.
            max_score = max(scores) # Contains minimum(lowest) grade
            min_score = min(scores) # Contains max(highest) grade
            max_terms = []
            min_terms = []
            for row in current_data:
                if max_score == int(row[7]):
                    if not (row[2] in max_terms): # If term recorded in csv is not found in the max_terms container. Append it to the list.
                        max_terms.append(row[2])
                if min_score == int(row[7]):
                    if not (row[2] in min_terms): # If term recorded in csv is not found in the min_terms container. Append it to the list.
                        min_terms.append(row[2])

            # Format to which the data is to be presented.
            str_container += f"""============================================================
***********        {level} Level        ***********
============================================================
Overall average (major and minor) for all terms: {overall_average}\n"""
            for i in range(max_term):
                term_grades = []
                for row in current_data :
                    if int(row[2]) == i+1 and row[1] == record[6]:
                        term_grades.append(int(row[7]))
                str_container += f"Term {i+1}: {statistics.mean(term_grades)}\n"
            str_container += f"""Maximum grade(s) and in which term(s): {max_score} in term {max_terms}
Minimum grade(s) and in which term(s): {min_score} in term {min_terms}
Do you have any repeated course(s)? {is_repeating}\n
            """


            text_container += str_container # Concatinates the format to the text_container to be presented in the text.
            print(str_container)

        return text_container # Returns the text_container.
    
    def majorTranscriptFeature(current_records_major): # Presents the major transcript of the student (major courses, the average of major courses in each term and the overall major average for all terms up to the last term.)
        current_id = current_records_major[0][1]
        # data = np.loadtxt('{}.csv'.format(current_id), dtype=str, delimiter=',', skiprows=1)
        data = np.loadtxt('201008000.csv', dtype=str, delimiter=',', skiprows=1)
        with open("std201008000MajorTranscript.txt", "w") as file: # Saves the data in the text specified.
            file.write(Program.printMajorTranscriptFeature(current_records_major, data))


    def printMajorTranscriptFeature(statistics_records, current_data): 
        text_container = "" # Contains the data to be saved in the text based on the format presented by the str_container.
        for degree in statistics_records:
            name = degree[2] # Contains student's name, recorded in the 3rd column of the csv file.
            college = degree[3] # Contains student's college, recorded in the 4th column of the csv file.
            major = degree[7] # Contains student's major subject, recorded in the 8th column of the csv file.
            level = degree[5] # Contains student's level, recorded in the 6th column of the csv file.
            stdID = degree[1] # Contains student's ID, recorded in the 2nd column of the csv file.
            department = degree[4] # Contains student's department, recorded in the 5th column of the csv file.
            minor = degree[8] # Contains student's minor subject, recorded in the 9th column of the csv file.
            term_numbers = degree[9] # Contains student's terms, recorded in the 10th column of the csv file.
            str_container = "" # Contains format for which the first(Header) information is to be presented.
            str_container += f"{f'Name: {name}':<35}{f'stdID: {stdID}':<50}\n"
            str_container += f"{f'College: {college}':<35}{f'Department: {department}':<50}\n"
            str_container += f"{f'Major: {major}':<35}{f'Minor: {minor}':<50}\n"
            str_container += f"{f'Level: {level}':<35}{f'Number of terms: {term_numbers}':<50}\n"
            max_term = 0
            if "BS" in degree[6]:
                for row in current_data:
                    if "BS" in row[1]:
                        level = "Undergraduate"
                        if int(row[2]) > max_term: # Will check if the current term being checked is the highest term and will be stored as the max_term.
                            max_term = int(row[2])
            elif "M" in degree[6]:
                for row in current_data:
                    if "M" in row[1]:
                        level = "Graduate(M)"
                        if int(row[2]) > max_term: # Will check if the current term being checked is the highest term and will be stored as the max_term.
                            max_term = int(row[2])
            elif "D" in degree[6]:
                for row in current_data:
                    if "D" in row[1]:
                        level = "Graduate(D)"
                        if int(row[2]) > max_term: # Will check if the current term being checked is the highest term and will be stored as the max_term.
                            max_term = int(row[2])
            print(str_container)
            
            for i in range(max_term):
                term_rows = []
                overall_average = []
                major_average = []
                term_container = "" # Contains format for which the second(main) information is to be presented.
                term_container += f"============================================================\n"
                term_container += f"***************       Term {i+1}     ***************\n"
                term_container += f"============================================================\n"
                for row in current_data:
                    if int(row[2]) == i+1 and degree[6] == row[1]:
                        term_rows.append(row)


                term_container += f"{f'course ID':<15}{f'course name':<15}{f'credit hours':<15}{f'grade':<15}\n"
                for filtered_row in term_rows:
                    term_container += f"{f'{filtered_row[4]}':<15}{f'{filtered_row[3]}':<15}{f'{filtered_row[6]}':<15}{f'{filtered_row[7]}':<15}\n"
                    if filtered_row[5] == "Major": 
                        major_average.append(int(filtered_row[7]))
                    overall_average.append(int(filtered_row[7]))
                term_container += f"Major Average = {statistics.mean(major_average)}                   Overall Average = {statistics.mean(overall_average)}"
                print(term_container)
            

            text_container += str_container # Concatinates the format to the text_container to be presented in the text.
        return text_container # Returns the text_container.

    
if __name__ == "__main__":
    Program.startFeature()