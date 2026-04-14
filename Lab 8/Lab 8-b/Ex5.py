# Program to remove any scores from a list that are below 50.
 
scores = [60, 45, 30, 85, 10, 90] 
scores_list = []

while scores: 
    score = scores.pop(0) 
    if score >= 50: 
        scores_list.append(score)
print(scores_list)