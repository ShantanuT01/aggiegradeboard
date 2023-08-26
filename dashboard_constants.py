import pandas as pd
from dotenv import load_dotenv
load_dotenv()
from kaggle.api.kaggle_api_extended import KaggleApi
# constants for columns
PROFESSOR_COURSE_COLS = "subject_code,course_number,a%,b%,c%,d%,f%,q%,i%,s%,u%,x%,mean_gpa,q_gpa,total_students".split(',')
AEFIS_QUESTIONS_COLS = {
     "Based on what the instructor(s) communicated, and the information provided in the course syllabus, I understood what was expected of me.":"expected_1,expected_2,expected_3".split(','),
     "This course helped me learn concepts or skills as stated in course objectives/outcomes.":"objectives_1,objectives_2,objectives_3,objectives_4".split(','),
     "In this course, I engaged in critical thinking and/or problem solving.":"critical_thinking_1,critical_thinking_2,critical_thinking_3,critical_thinking_4".split(','),
     "Please rate the organization of this course.":"organization_1,organization_2,organization_3,organization_4".split(','),
     "In this course, I learned to critically evaluate diverse ideas and perspectives.":"diverse_1,diverse_2,diverse_3,diverse_4,diverse_5,diverse_0".split(','),
     "Feedback in this course helped me learn. Please note, feedback can be either informal (e.g., in class discussion, chat boards, think-pair-share, office hour discussions, help sessions) or formal (e.g., written or clinical assessments, review of exams, peer reviews, clicker questions).":"feedback_1,feedback_2,feedback_3,feedback_4,feedback_5,feedback_6".split(',')

}

KAGGLE_DATASET_NAME = "sst001/texas-a-and-m-university-grades-and-aefis-dataset"
AEFIS_QUESTIONS = [key + "(Multi-Choice, Single Answer)" for key in AEFIS_QUESTIONS_COLS.keys()]
SUBJECT_CODE = "subject_code"
COURSE_NUMBER = "course_number"
PROF_NAME = "professor_name"
AEFIS_MEAN_COLS = ["mean_expected","mean_objectives","mean_critical_thinking","mean_organization","mean_diverse","mean_feedback","total_surveys","surveys_completed"]
COMMENT = "comment"
ALL_TIME = "ALL TIME"
VALUE = "value"
SEMESTER = "semester"
TERM = "term"
YEAR = "year"
SEMESTER_CODE = "semester_code"
STUDENTS = "students"
CHOICE = "choices"
QUESTION = "question"

# color related
COLOR = "color"
CYAN = '#19D3F3'
RED = '#EF553B'
ORANGE = '#FFA15A'
PURPLE = '#AB63FA'
BLUE = '#636EFA'
GREEN = '#00CC96'

# copied directly from the JSON source data
AEFIS_CHOICE_MAPPINGS = {
      "Based on what the instructor(s) communicated, and the information provided in the course syllabus, I understood what was expected of me.": {
                "No, I did not understand what was expected of me.": {
                    VALUE: 1,
                    COLOR: RED,
                },
                "I partially understood what was expected of me.": {
                    VALUE: 2,
                    COLOR: BLUE,
                },
                "Yes, I understood what was expected of me.": {
                    VALUE: 3,
                    COLOR: GREEN,
                },
            },
            "This course helped me learn concepts or skills as stated in course objectives/outcomes.": {
                "This course did not help me learn the concepts or skills.": {
                    VALUE: 1,
                    COLOR: RED,
                   
                },
                "This course only slightly helped me learn the concepts or skills.": {
                    VALUE: 2,
                    COLOR: ORANGE,
                    
                },
                "This course moderately helped me learn the concepts or skills.": {
                    VALUE: 3,
                    COLOR: BLUE,
                    
                },
                "This course definitely helped me learn the concepts or skills.": {
                    VALUE: 4,
                    COLOR: GREEN,
                    
                }
            },
            "In this course, I engaged in critical thinking and/or problem solving.": {
                "Never": {
                    VALUE: 1,
                    COLOR: RED,
                    
                },
                "Seldom": {
                    VALUE: 2,
                    COLOR: ORANGE,
                   
                },
                "Often": {
                    VALUE: 3,
                    COLOR: BLUE,
                    
                },
                "Frequently": {
                    VALUE: 4,
                    COLOR: GREEN
                   
                },
               
            },
            "Please rate the organization of this course.": {
                "Not at all organized": {
                    VALUE: 1,
                    COLOR: RED,
                   
                },
                "Slightly organized": {
                    VALUE: 2,
                    COLOR: ORANGE
                    
                },
                "Moderately organized": {
                    VALUE: 3,
                    COLOR: BLUE,
                },
                "Very well organized": {
                    VALUE: 4,
                    COLOR: GREEN
                    
                }
            },
            "In this course, I learned to critically evaluate diverse ideas and perspectives.": {
                "Not Applicable": {
                    VALUE: 0,
                    COLOR: CYAN
                },
                "Strongly agree": {
                    VALUE: 5,
                    COLOR: GREEN,
                },
                "Agree": {
                    VALUE: 4,
                    COLOR: BLUE
                    
                },
                "Neither agree nor disagree": {
                    VALUE: 3,
                    COLOR: PURPLE
                   
                },
                "Disagree": {
                    VALUE: 2,
                    COLOR: ORANGE, 
                },
                "Strongly disagree": {
                    VALUE: 1,
                    COLOR: RED
                }
            },
            "Feedback in this course helped me learn. Please note, feedback can be either informal (e.g., in class discussion, chat boards, think-pair-share, office hour discussions, help sessions) or formal (e.g., written or clinical assessments, review of exams, peer reviews, clicker questions).": {
                "No feedback was provided.": {
                    VALUE: 1,
                    COLOR: RED
                   
                },
                "Feedback provided was not at all helpful.": {
                    VALUE: 2,
                    COLOR: ORANGE
                 
                },
                "Feedback provided was only slightly helpful.": {
                    VALUE: 3,
                    COLOR: PURPLE
                   
                },
                "Feedback provided was moderately helpful.": {
                    VALUE: 4,
                    COLOR: CYAN
                  
                },
                "Feedback provided was very helpful.": {
                    VALUE: 5,
                    COLOR: BLUE,
                    
                },
                "Feedback provided was extremely helpful.": {
                    VALUE: 6,
                    COLOR: GREEN
                 
                },
               
            }
}



# helper functions

def query_frame(params, dataframe):
    query_string = list()
    for param in params:
        value = params[param]
        if isinstance(value, str):
            query_string.append(f"{param} == '{value}' ")
        else:
            query_string.append(f"{param} == {value} ")
    query_string = " and ".join(query_string)
    return pd.DataFrame(dataframe.query(query_string))


def download_kaggle_data():
    api = KaggleApi()
    api.authenticate()
    api.dataset_download_files(KAGGLE_DATASET_NAME, unzip=True)
