import myfitnesspal
import plotly_express as px
from calendar import monthrange

EXER_CARDIO = 0 #constant representing cardio in exercises
EXER_STR = 1 #constant represending strength training in exercises

EXERCISE_NAME = 'Bench Press, Barbell' # exercise name, for testing

def calculate_1rm(weight, reps): # returns an estimated 1rm based on weight and reps
    return weight * reps * 0.0333 + weight
    #formula used is from http://www.crossfitepoc.com/calculators/1rm-estimate

def calculate_1rm_day(exercise_data, exercise_name): #returns the highest calculated 1rm on a given day
    max_1rm: int = 0
    for i in range(0, len(exercise_data)):
        if (exercise_name == exercise_data[i]['name']):  # exercise name matches requested one
            weight = exercise_data[i]['nutrition_information']['weight/set']
            reps = exercise_data[i]['nutrition_information']['reps/set']
            max_1rm = max(max_1rm, calculate_1rm(weight, reps))
    return max_1rm

client = myfitnesspal.Client(username, password) # myfitnesspal username, password

# used for testing
year = 2019
month = 12
num_days_month = monthrange(year, month)[1] # number of days in the given month

# for data storage
dates = []
for i in range(1, num_days_month+1):
    dates.append(i)
one_rep_max_data = [0] * num_days_month

for date in range(1, num_days_month):
    date_full = [year, month, date]
    day_data = client.get_date(date_full[0], date_full[1], date_full[2])
    print("Getting exercise data for " + str(date_full))

    exercises_strength = day_data.exercises[EXER_STR].get_as_list()

    one_rep_max_data[date] = calculate_1rm_day(exercises_strength, EXERCISE_NAME)

    # keeping this for the time being, but is unnecessarily inefficient
    #for i in range(0, len(exercises_strength) -1):
     #   if(exercise_name == exercises_strength[i]['name']):
      #      one_rep_max = calculate_1rm_day(exercises_strength, exercise_name)
       #     print(str(exercise_name) + "One-rep Max: " + str(one_rep_max))
        #    one_rep_max_data[date] = one_rep_max
         #   break

dates_clean = []
one_rep_max_data_clean = []
# cleaning up data so only non-zero values are graphed
for i in range(0, num_days_month):
    if(one_rep_max_data[i] != 0):
        dates_clean.append(dates[i])
        one_rep_max_data_clean.append(one_rep_max_data[i])

fig = px.scatter(x = dates_clean, y = one_rep_max_data_clean)
fig.show()









