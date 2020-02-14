import myfitnesspal
import plotly_express as px
from calendar import monthrange
import time

EXER_CARDIO = 0  # constant representing cardio in exercises; not currently needed
EXER_STR = 1  # constant representing strength training in exercises

INDEX_DAYS = 1  # represents index of days in monthrange calculation

EXERCISE_NAME_0 = 'Bench Press, Barbell'  # exercise name, for testing
EXERCISE_NAME_1 = 'Squat'  # second exercise name, for testing with lists

# lists of example data to test with
TEST_EXERCISE_NAME_0_DATA = [0, 175.64600000000002, 0, 0, 0, 186.655, 0, 0, 181.312, 0, 0, 0, 191.988, 0, 0, 186.978, 0, 0, 0, 197.321, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
TEST_EXERCISE_NAME_1_DATA = [0, 0, 274.975, 0, 0, 0, 214.4805, 0, 0, 280.4745, 0, 0, 0, 0, 0, 0, 280.4745, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


class Exercise:  # stores exercise data

    def __init__(self, exercise_name):
        self.name = exercise_name
        self.exercise_1rm_data = []  # one rep max data
        self.exercise_dates_clean = []  # graphing data, with days where exercise wasn't done removed
        self.exercise_1rm_data_clean = []  # graphing data, with days where exercise wasn't done removed

    def append_1rm(self, day_data_overall):
        # appends one rep max data with the 1rm for a given date
        one_rep_max = calculate_1rm_day(day_data_overall, self.name)
        self.exercise_1rm_data.append(one_rep_max)

    def clean(self):
        # cleans data for graphing
        for i in range(0, len(self.exercise_1rm_data)-1):
            if self.exercise_1rm_data[i] != 0:
                self.exercise_dates_clean.append(i+1)  # date
                self.exercise_1rm_data_clean.append(self.exercise_1rm_data[i])

    def test_populate_1rm(self, test_1rm_data):  # populates with test data
        self.exercise_1rm_data = test_1rm_data


def calculate_1rm(weight, reps):  # returns an estimated 1rm based on weight and reps
    return weight * reps * 0.0333 + weight
    # formula used is from http://www.crossfitepoc.com/calculators/1rm-estimate


def calculate_1rm_day(exercise_data, exercise_name):  # returns the highest calculated 1rm on a given day
    max_1rm: int = 0
    for i in range(0, len(exercise_data)):
        if exercise_name == exercise_data[i]['name']:
            weight = exercise_data[i]['nutrition_information']['weight/set']
            reps = exercise_data[i]['nutrition_information']['reps/set']
            max_1rm = max(max_1rm, calculate_1rm(weight, reps))
    return max_1rm


def populate_1rm_month(client_name, exercises, year, month):  # to populate data in a list of Exercises
    num_days_month = monthrange(year, month)[INDEX_DAYS]  # calculates days using given month, year

    for date in range(1, num_days_month + 1):  # populate 1rm data
        date_full = [year, month, date]
        day_data = client_name.get_date(date_full[0], date_full[1], date_full[2])
        print('Getting exercise data for ' + str(date_full))

        exercises_strength = day_data.exercises[EXER_STR].get_as_list()

        for i in range(0, len(exercises)):
            exercises[i].append_1rm(exercises_strength)


# set up client
print('Setting up client...')
client = myfitnesspal.Client(username, password)   # myfitnesspal username, password

test_exer = [Exercise(EXERCISE_NAME_0), Exercise(EXERCISE_NAME_1)]  # list to store exercises

print('Populating 1RMs...')
populate_1rm_month(client, test_exer, 2019, 12)

# For testing
# test_exer[0].test_populate_1rm(TEST_EXERCISE_NAME_0_DATA)
# test_exer[1].test_populate_1rm(TEST_EXERCISE_NAME_1_DATA)

for i in range(0, len(test_exer)):  # Clean up data for graphing
    test_exer[i].clean()

# Graph data
print('Graphing...')

# The delays seem to fix an error where the first graph doesn't always display
time.sleep(1)
fig = px.scatter(x=test_exer[0].exercise_dates_clean, y=test_exer[0].exercise_1rm_data_clean)
fig.show()

time.sleep(1)
fig2 = px.scatter(x=test_exer[1].exercise_dates_clean, y=test_exer[1].exercise_1rm_data_clean)
fig2.show()










