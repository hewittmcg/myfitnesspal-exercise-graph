import myfitnesspal
from calendar import monthrange

EXER_CARDIO = 0 #constant representing cardio in exercises
EXER_STR = 1 #constant represending strength training in exercises

client = myfitnesspal.Client('username', 'password') #username + password

year = 2020
month = 2
num_days_month = monthrange(year, month)[1] #number of days in the given month
print(num_days_month)

for date in range(1, num_days_month):
    date_full = [2020, month, date]
    day_data = client.get_date(date_full[0], date_full[1], date_full[2])
    print("Getting exercise data for " + str(date_full))

    exercises_strength = day_data.exercises[EXER_STR].get_as_list()
    #print(exercises_strength)
    if(len(exercises_strength) != 0): #only prints if there's data
        for i in range(0, len(exercises_strength)):
            print(exercises_strength[i])
    else: #no data available
        print("No data")




