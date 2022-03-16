import utils
from datetime import datetime

def test_get_work_hour_salaries():
  assert utils.get_work_hour_salaries("TU") == {"00:01 - 09:00" : "25 USD","09:01 - 18:00" : "15 USD","18:01 - 00:00" : "20 USD"}
  assert utils.get_work_hour_salaries("SA") == {"00:01 - 09:00" : "30 USD","09:01 - 18:00" : "20 USD","18:01 - 00:00" : "25 USD"}
  assert utils.get_work_hour_salaries("XX") == {}

def test_get_next_day_worked():
  assert utils.get_next_day_worked("SU") == "MO"
  assert utils.get_next_day_worked("MO") == "TU"

def test_calculate_amount_to_pay_by_hour():
  assert utils.calculate_amount_to_pay_by_hour(datetime(1900, 1, 1, 23, 1, 0),{"00:01 - 09:00" : "25 USD","09:01 - 18:00" : "15 USD","18:01 - 00:00" : "20 USD"}) == 20

if __name__ == "__main__":
  test_get_work_hour_salaries()
  test_get_next_day_worked() 
  test_calculate_amount_to_pay_by_hour()
  print("Everything passed")