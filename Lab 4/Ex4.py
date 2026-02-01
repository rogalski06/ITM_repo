# Try to append to a tuple, it wont work
# Name: Katherine Rogalski
# Date: Jan. 31. 2026

survey_responses = (1012, 1035, 1021, 1053)
print("Original survey responses tuple:", survey_responses)
# survey_responses.append(1060)  # This will raise an AttributeError
survey_responses = survey_responses + (1054,)
print("After adding 1054 to the tuple:", survey_responses)