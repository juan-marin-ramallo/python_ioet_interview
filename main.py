from datetime import timedelta
import utils

'''
This method calculte for every employee the total amount to pay on base a days and times worked
Receive like parameter a String with employee information. Example:
RENE=MO10:00-12:00,TU10:00-12:00,TH01:00-03:00,SA14:00-18:00,SU20:00-21:00
'''
def calculate_pay_by_employee(employee_job_schedule):
  #get entity with employe and schedule worked
  employee_entity = utils.get_employee_info(employee_job_schedule)
  #Initialize total to pay to employee 
  total_to_pay = 0

  #Iterate for every day worked indicated in schedule
  for day_time_worked_entity in employee_entity.schedule_worked:
    #Get the dictionary with work hour salaries according to day_worked
    work_hour_salaries = utils.get_work_hour_salaries(day_time_worked_entity.day_worked)
      
    if not work_hour_salaries:
      print("The day %s is not a valid day. Please check input data" % day_time_worked_entity.day_worked)
      break
      
    #Add 1 minute to make match with start time from work_hour_salaries
    if(day_time_worked_entity.start_time_worked.minute == 0):
      iterate_time_worked = day_time_worked_entity.start_time_worked + timedelta(minutes=1)
    else:
      iterate_time_worked = day_time_worked_entity.start_time_worked
      
    #Add 1 day to end_time_worked if it is equal to zero
    if(day_time_worked_entity.end_time_worked.hour == 0):
      day_time_worked_entity.end_time_worked = day_time_worked_entity.end_time_worked + timedelta(days=1)

    #Iterate every hour worked for each day_worked
    while(iterate_time_worked < day_time_worked_entity.end_time_worked): 
      amount_to_pay_by_hour = utils.calculate_amount_to_pay_by_hour(iterate_time_worked,work_hour_salaries)

      if amount_to_pay_by_hour > 0:
        total_to_pay = total_to_pay + amount_to_pay_by_hour

      #Add 1 hora to iterate_time_worked to continue to the next hour worked
      iterate_time_worked = iterate_time_worked + timedelta(hours=1)      

    #Validate if the minute of end_time_worked is greater than 0 to pay extra hour
    if(day_time_worked_entity.end_time_worked.minute > 0):
      iterate_time_worked = day_time_worked_entity.end_time_worked

      #Validate if the hour is equal 0 to get the next day and the work_hour_salaries for this next day
      if(day_time_worked_entity.end_time_worked.hour == 0):
        iterate_time_worked = day_time_worked_entity.end_time_worked - timedelta(days=1)
        next_day_worked = utils.get_next_day_worked(day_time_worked_entity.day_worked)
        work_hour_salaries = utils.get_work_hour_salaries(next_day_worked)

      #Calculate the amount to pay according to iterate_time_worked and work_hour_salaries
      amount_to_pay_by_hour = utils.calculate_amount_to_pay_by_hour(iterate_time_worked,work_hour_salaries)

      if amount_to_pay_by_hour > 0:
        total_to_pay = total_to_pay + amount_to_pay_by_hour

  print("The amount to pay %s is: %d USD" %(employee_entity.name,total_to_pay))

"""
Main method to read job_schedule.txt file and for every line call to calculate_pay_by_employee method.
For every line, this method show the amount to pay for each employee
"""
if __name__ == "__main__":
  try:  
    #calculate_pay_by_employee("KARLA=TH23:00-00:00")
    with open('job_schedule.txt') as job_schedule_file:
      for job_schedule_line in job_schedule_file:
        calculate_pay_by_employee(job_schedule_line.replace("\n", ""))
  except Exception as ex:
    print("Error catched: {0}".format(ex))