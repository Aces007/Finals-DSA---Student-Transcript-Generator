import numpy as np
import time
from datetime import datetime
import sys
import os
import statistics
import math

class Program:
    timestamps = []
    BOLD = '\033[1m'
    END = '\033[0m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    CYAN = '\033[96m'

    def readData(): # This is the csv reader, it will read the data inside the csv file and will be used as basis for the program.
        data = np.loadtxt('studentDetails.csv', dtype=str, delimiter=',', skiprows=1)
        # for each_data in data:
        #     print(each_data)
        return data
    
    def sleep():
        for pause_in_seconds in range(3, 0, -1):
            print (f"{Program.BOLD}{Program.GREEN}Loading in {pause_in_seconds} second ...{Program.END}")
            time.sleep(1)

    def clear():
        clear = lambda: os.system("cls")
        clear()

    def errorMessage():
        return f'{Program.BOLD}{Program.RED}[Error] Invalid input. Please try again.{Program.END}'

    def startFeature():
        Program.clear()
        levels_chosen = [] # Storage of the levels chosen  
        # This is where the user will choose the level of the record he/she is looking for
        initial_student_level = input(f"{Program.BOLD}{Program.YELLOW}Student Level:{Program.END}\n[U] Undergraduate\n[G] Graduate\n[B] Both?\nEnter student level: ") 
        if initial_student_level.upper() == "U": # If undergraduate array will store choice then will look for the record using getStudentID
            levels_chosen.append("U")
            Program.getStudentID(levels_chosen)
        elif initial_student_level.upper() == "G": # If graduate prompt asks what graduate level user is, if M or D or Both
            Program.clear()
            # Then array stores choice then will look for the studentID using the choice.
            secondary_student_level = input(f"{Program.BOLD}{Program.YELLOW}Graduate Level:{Program.END}\n[M] Master\n[D] Doctorate\n[B0] Both?\nEnter graduate level: ")
            if secondary_student_level.upper() == "M" or secondary_student_level.upper() == "B0":
                levels_chosen.append("M")
            if secondary_student_level.upper() == "D" or secondary_student_level.upper() == "B0":
                levels_chosen.append("D")
            Program.getStudentID(levels_chosen)

        elif initial_student_level.upper() == "B": # If both undergraduate and graduate, user's first choice (U) is stored then prompt
            Program.clear()
            # asks whether graduate level is M, D, or Both then 2nd choice is stored then studentID is looked for using the getStudentID.
            levels_chosen.append("U")
            secondary_student_level = input(f"{Program.BOLD}Graduate Level:{Program.END}\n[M] Master\n[D] Doctorate\n[B0] Both?\nEnter graduate level: ")
            if secondary_student_level.upper() == "M" or secondary_student_level.upper() == "BO":
                levels_chosen.append("M")
            if secondary_student_level.upper() == "D" or secondary_student_level.upper() == "BO":
                levels_chosen.append("D")
            Program.getStudentID(levels_chosen)

    def getStudentID(student_level): # Will look for the student ID based on your choice of student level in the beginning.
        try:
            Program.clear()
            transcript_records = Program.readData() # Stores the data on csv
            student_id = input("Enter student ID: ") # Prompt gets the StudentID of user
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

        except ValueError as e: # If data provided is not in saved records, error will be raised.
            print("No corresponding records found.\n\n")
            print(e)
            Program.startFeature()

    def menuFeature(corresponding_records): # This will launch if all the data provided by the user matches the ones in record.
        while True:
            try:
                print("==================================================")
                print(f"{Program.BOLD}Student Transcription Generation System{Program.END}")
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
                choice = int(input("Enter your feature: "))
                Program.clear()
                if choice == 1:
                    Program.getTimeStamp('Details', Program.timestamps)
                    Program.detailsFeature(corresponding_records)
                elif choice == 2:
                    Program.getTimeStamp('Statistics', Program.timestamps)
                    Program.statisticsFeature(corresponding_records)
                elif choice == 3:
                    Program.getTimeStamp('Major', Program.timestamps)
                    Program.majorTranscriptFeature(corresponding_records)
                elif choice == 4:
                    Program.getTimeStamp('Minor', Program.timestamps)
                    Program.minorTranscriptFeature(corresponding_records)
                elif choice == 5:
                    Program.getTimeStamp('Full', Program.timestamps)
                    Program.fullTranscriptFeature(corresponding_records)
                elif choice == 6:
                    Program.previousRequestFeature(corresponding_records)
                elif choice == 7:
                    Program.newStudentFeature()
                elif choice == 8:
                    Program.terminateFeature()
                else:
                    raise ValueError
            except ValueError:
                Program.clear()
                print(Program.errorMessage())
                Program.menuFeature(corresponding_records)

    def detailsFeature(current_records): # Present student details, prints them in format then stores them in a list.
        Program.clear()
        name = current_records[0][2]
        stdID = current_records[0][1]
        levels = ", ".join(record[5] for record in current_records) 
        term_numbers = ", ".join(record[9] for record in current_records)
        colleges = ", ".join(record[3] for record in current_records)
        departments =", ".join(record[4] for record in current_records)
        print(Program.printDetails(name, stdID, levels, term_numbers, colleges, departments))
        with open("std{}details.txt".format(stdID), "w") as file:
            file.write(Program.printDetails(name, stdID, levels, term_numbers, colleges, departments))
        Program.sleep()
    
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
            file.write(str(Program.printMajorTranscriptFeature(current_records_major, data)))

    def printMajorTranscriptFeature(statistics_records, current_data): 
        text_container = "" # Contains the data to be saved in the text based on the format presented by the str_container.
        levels = list(set([level[5] for level in statistics_records]))
        levels.sort(reverse=True)
        for level in levels:
            overall_average = []
            header_value = Program.transcriptHeader(statistics_records, level)
            text_container += header_value[0]
            print(header_value[0])
            for i in range(header_value[1]): #This is iterating to each term
                major_average = []
                term_str_container = ""
                term_str_container += f"====================================================\n"
                term_str_container += f"****************       Term {i+1}       ****************\n"
                term_str_container += f"====================================================\n"
                term_str_container += f"{f'Course ID':<15}{f'Course name':<15}{f'Credit hours':<15}{f'Grade':<15}\n"
                for row in current_data:
                    if row[0] == level and "Major" == row[5]:  
                        if int(row[2]) == i+1:
                            major_average.append(int(row[7]))
                            term_str_container += f"{f'{row[4]}':<15}{f'{row[3]}':<15}{f'{row[6]}':<15}{f'{row[7]}':<15}\n"
                        overall_average.append(int(row[7]))
                term_str_container += f"{f'Major Average = {statistics.mean(major_average)}':<30}{f'Overall Average = {statistics.mean(overall_average)}':<30}\n"
                text_container += term_str_container
                print(term_str_container)
            footer_container = ''
            footer_container += f"====================================================\n"
            footer_container += f'*******   End of transcript for level ({level})   *******\n'
            footer_container += f"====================================================\n"
            text_container += footer_container
            print(footer_container)

        return text_container

    def minorTranscriptFeature(current_records_minor):
        current_id = current_records_minor[0][1]
        # data = np.loadtxt('{}.csv'.format(current_id), dtype=str, delimiter=',', skiprows=1)
        data = np.loadtxt('201008000.csv', dtype=str, delimiter=',', skiprows=1)
        with open("std201008000MinorTranscript.txt", "w") as file: # Saves the data in the text specified.
            file.write(str(Program.printMinorTranscriptFeature(current_records_minor, data)))

    def printMinorTranscriptFeature(statistics_records, current_data):
        text_container = "" # Contains the data to be saved in the text based on the format presented by the str_container.
        levels = list(set([level[5] for level in statistics_records]))
        levels.sort(reverse=True)
        for level in levels:
            overall_average = []
            header_value = Program.transcriptHeader(statistics_records, level)
            text_container += header_value[0]
            print(header_value[0])
            for i in range(header_value[1]): #This is iterating to each term
                minor_average = []
                term_str_container = ""
                term_str_container += f"====================================================\n"
                term_str_container += f"****************       Term {i+1}       ****************\n"
                term_str_container += f"====================================================\n"
                term_str_container += f"{f'Course ID':<15}{f'Course name':<15}{f'Credit hours':<15}{f'Grade':<15}\n"
                for row in current_data:
                    if row[0] == level and "Minor" == row[5]:  
                        if int(row[2]) == i+1:
                            minor_average.append(int(row[7]))
                            term_str_container += f"{f'{row[4]}':<15}{f'{row[3]}':<15}{f'{row[6]}':<15}{f'{row[7]}':<15}\n"
                        overall_average.append(int(row[7]))
                term_str_container += f"{f'Minor Average = {statistics.mean(minor_average)}':<30}{f'Overall Average = {statistics.mean(overall_average)}':<30}\n"
                text_container += term_str_container
                print(term_str_container)
            footer_container = ''
            footer_container += f"====================================================\n"
            footer_container += f'*******   End of transcript for level ({level})   *******\n'
            footer_container += f"====================================================\n"
            text_container += footer_container
            print(footer_container)

        return text_container

    def fullTranscriptFeature(current_records_full):
        current_id = current_records_full[0][1]
        # data = np.loadtxt('{}.csv'.format(current_id), dtype=str, delimiter=',', skiprows=1)
        data = np.loadtxt('201008000.csv', dtype=str, delimiter=',', skiprows=1)
        with open("std201008000MajorTranscript.txt", "w") as file: # Saves the data in the text specified.
            file.write(str(Program.printFullTranscriptFeature(current_records_full, data)))

    def printFullTranscriptFeature(statistics_records, current_data):
        Program.requestCounter(1)
        Program.previousRequestFeature('Major', timestamp)

        text_container = "" # Contains the data to be saved in the text based on the format presented by the str_container.
        levels = list(set([level[5] for level in statistics_records]))
        levels.sort(reverse=True)
        for level in levels:
            overall_average = []
            header_value = Program.transcriptHeader(statistics_records, level)
            text_container += header_value[0]
            print(header_value[0])
            for i in range(header_value[1]): #This is iterating to each term
                minor_average = []
                major_average = []
                term_average = []
                term_str_container = ""
                term_str_container += f"====================================================\n"
                term_str_container += f"****************       Term {i+1}       ****************\n"
                term_str_container += f"====================================================\n"
                term_str_container += f"{f'Course ID':<15}{f'Course name':<15}{f'Credit hours':<15}{f'Grade':<15}\n"
                for row in current_data:
                    if row[0] == level and "Minor" == row[5]:  
                        if int(row[2]) == i+1:
                            minor_average.append(int(row[7]))
                            term_str_container += f"{f'{row[4]}':<15}{f'{row[3]}':<15}{f'{row[6]}':<15}{f'{row[7]}':<15}\n"
                            term_average.append(int(row[7]))
                        overall_average.append(int(row[7]))
                    if row[0] == level and "Major" == row[5]:  
                        if int(row[2]) == i+1:
                            major_average.append(int(row[7]))
                            term_str_container += f"{f'{row[4]}':<15}{f'{row[3]}':<15}{f'{row[6]}':<15}{f'{row[7]}':<15}\n"
                            term_average.append(int(row[7]))
                        overall_average.append(int(row[7]))
                term_str_container += f"{f'Major Average = {statistics.mean(major_average)}':<30}{f'Minor Average = {statistics.mean(minor_average)}':<30}\n"
                term_str_container += f"{f'Term Average = {statistics.mean(term_average)}':<30}{f'Overall Average = {statistics.mean(overall_average)}':<30}\n"
                text_container += term_str_container
                print(term_str_container)
            footer_container = ''
            footer_container += f"====================================================\n"
            footer_container += f'*******   End of transcript for level ({level})   *******\n'
            footer_container += f"====================================================\n"
            text_container += footer_container
            print(footer_container)
        Program.sleep()

    def transcriptHeader(statistics_records, current_level): # Returns all necessary information to be printed
        name = statistics_records[0][2]
        stdID = statistics_records[0][1]
        term_numbers = 0
        departments = []
        minors = []
        majors = []
        colleges = []
        for row in statistics_records:
            if row[5] == current_level:
                departments.append(row[4])
                minors.append(row[8])
                majors.append(row[7])
                colleges.append(row[3])
                term_numbers = max(term_numbers, int(row[9]))
        colleges_str = ', '.join([college for college in colleges])
        departments_str = ', '.join([department for department in departments])
        majors_str = ', '.join([major for major in majors])
        minors_str = ', '.join([minor for minor in minors])

        str_container = "" # Contains format for which the first(Header) information is to be presented.
        str_container += f""
        str_container += f"\n{f'Name: {name}':<35}{f'stdID: {stdID}':<50}\n"
        str_container += f"{f'College: {colleges_str}':<35}{f'Department: {departments_str}':<50}\n"
        str_container += f"{f'Major: {majors_str}':<35}{f'Minor: {minors_str}':<50}\n"
        str_container += f"{f'Level: {current_level}':<35}{f'Number of terms: {term_numbers}':<50}\n"
        return [str_container, int(term_numbers)]

    def previousRequestFeature(previous_records):
        current_id = previous_records[0][1]
        record = Program.printRequests(Program.timestamps, current_id)
        with open(f"std{current_id}PreviousRequests.txt", "w") as file: # Saves the data in the text specified.
            file.write(record)
        print(record)
    
        #Function that will provide date and time to the system

    def getDataAndTime():
        today = datetime.today()
        now = datetime.now()
        date = (today.strftime("%d/%m/%Y"))
        time = (now.strftime("%H:%M"))
        return now,date,time

    # Function that will record the timestamps on every function in the system
    def getTimeStamp(request_type, timestamps):
        date_now = Program.getDataAndTime()[1]
        time_now = Program.getDataAndTime()[2]
        timestamp_array = timestamps.append((request_type,date_now,time_now))
        return timestamp_array

    # Function that will print all the student requests
    def printRequests(timestamps, current_id):
        if not os.path.isfile(f"std{current_id}PreviousRequests.txt"):
            lines = f'==================================================\n'
            lines += f"{f'Request':<20}{f'Date':<20}{f'Time':<10}\n"
            lines += f'=================================================='
        else:
            lines = ""
            with open(f"std{current_id}PreviousRequests.txt", "r") as file: 
                for line in file.readlines():
                    lines += line
        for request, date, time in timestamps:
            lines += f"\n{f'{request}':<20}{f'{date}':<20}{f'{time}':<10}"
        return lines
    
    def newStudentFeature():
        Program.clear()
        Program.startFeature()
    
    

    # def terminateFeature():
    #     sys.exit("Come again another day")

    # def requestCounter(num):
    #     request += num

if __name__ == "__main__":
    Program.startFeature()