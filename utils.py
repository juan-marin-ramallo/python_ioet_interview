from datetime import datetime, timedelta
import json
import entities

"""
get_employee_info function receive employee_job_schedule in format:
RENE=MO10:00-12:00,TU10:00-12:00,TH01:00-03:00,SA14:00-18:00,SU20:00-21:00
and returns an Entity object from Employee class using Pattern Singleton to avoid 
create new objects needlessly.
"""
def get_employee_info(employee_job_schedule):
  #Get name and schedule_worked from employee
  try:    
    #Left part from = is the name
    name = str(employee_job_schedule.split("=")[0])
    #Create a new collection using Iterator Pattern Design
    schedule_worked = entities.ScheduleWorkedCollection()
    #Right part from = is the schedule_worked separate with comma ,
    for day_time_worked_str in employee_job_schedule.split("=")[1].split(","):
      #Check if day_time_worked length is exactly 13 characters. Example: FR23:30-00:45
      if(len(day_time_worked_str) != 13):
        raise Exception('The length to describe day and time worked is incorrect') 
      #Extract 2 first digits to get the day initials
      day_worked = str(day_time_worked_str[:2])
      #Extract 11 last digits to get the time range worked
      time_worked = str(day_time_worked_str[-11:])
      #Get the start time worked from time range
      start_time_worked = datetime.strptime(time_worked.split("-")[0], "%H:%M")
      #Get the end time worked from time range
      end_time_worked = datetime.strptime(time_worked.split("-")[1], "%H:%M")
      #Create an objet Entity from class DayTimeWorked using day, start time and end time worked
      day_time_worked_entity = entities.DayTimeWorked(day_worked,start_time_worked,end_time_worked)
      #Add the day_time_worked_entity to the collection
      schedule_worked.add_item(day_time_worked_entity)
    #Create an object Entity from Employee class using Singleton Pattern
    return entities.Employee.instance(name, schedule_worked)
  except Exception as ex:
    raise Exception('There was a problem reading employee job schedule {0}: {1}'.format(employee_job_schedule,ex))
  
"""
Read json file with week and weekend hour salaries
using the json decode method load
"""
def load_work_hour_salaries():
  try:
    # Opening Work Hour Salaries JSON file
    with open('work_hour_salaries.json') as json_file:
      return json.load(json_file)
  except Exception as ex:
    raise Exception('There was a problem parsing JSON file: {0}'.format(ex))

"""
This Function return work hour salaries dictionary based on week or weekend day worked.
The Parameter received is a day with its 2 first initials
"""
def get_work_hour_salaries(day_worked):
  complete_work_hour_salaries = load_work_hour_salaries()

  if(day_worked == "SA" or day_worked == "SU"):
    return complete_work_hour_salaries['weekend']
  elif(day_worked == "MO" or day_worked == "TU" or day_worked == "WE" or day_worked == "TH" or day_worked == "FR"):
    return complete_work_hour_salaries['week']
  else:
    return {}

"""
This Function returns the next day of the week or weekend.
The Parameter received is a day with its 2 first initials
"""
def get_next_day_worked(day_worked):
  if day_worked == "SU":
    return "MO"
  if day_worked == "MO":
    return "TU"
  if day_worked == "TU":
    return "WE"
  if day_worked == "WE":
    return "TH"
  if day_worked == "TH":
    return "FR"
  if day_worked == "FR":
    return "SA"
  if day_worked == "SA":
    return "SU"
  

'''
This function return then amount to pay for every hour worked on base to time worked and to work hour salaries dictionary according if a week day o weekend day
'''
def calculate_amount_to_pay_by_hour(iterate_time_worked,work_hour_salaries):
  amount_to_pay_by_hour = 0
  
  try:
    #Iterate every schedule existing in work_hour_salaries
    for schedule_to_pay, amount_to_pay in work_hour_salaries.items():
      start_time_schedule = datetime.strptime(schedule_to_pay.split("-")[0].strip(), "%H:%M")
      end_time_schedule = datetime.strptime(schedule_to_pay.split("-")[1].strip(), "%H:%M")
  
      if(end_time_schedule.hour == 0):
        end_time_schedule = end_time_schedule + timedelta(days=1)
        
      if(iterate_time_worked >= start_time_schedule and iterate_time_worked < end_time_schedule):
        amount_to_pay_by_hour = int(amount_to_pay.split(" ")[0])
        break
  except Exception as ex:
    raise Exception('There was a problem calculating amount to pay by hour worked: {0}'.format(ex))
  
  return amount_to_pay_by_hour

