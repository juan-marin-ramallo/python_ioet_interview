from __future__ import annotations
from collections.abc import Iterable, Iterator
from typing import Any, List

"""
Class implemented Using Singleton Pattern and properties
"""
class Employee(object):
  _instance = None

  def set_name(self, name):
    self.__name= name
    
  def get_name(self):
    return self.__name

  name=property(get_name, set_name)

  def set_schedule_worked(self, schedule_worked):
    self.__schedule_worked= schedule_worked
    
  def get_schedule_worked(self):
    return self.__schedule_worked

  schedule_worked=property(get_schedule_worked, set_schedule_worked)
  
  def __init__(self):
    raise RuntimeError('Call instance() instead')
  
  @classmethod
  def instance(cls,name,schedule_worked):    
    if cls._instance is None:
      cls._instance = cls.__new__(cls)
    cls.__name = name
    cls.__schedule_worked = schedule_worked
    return cls._instance

"""
Class implemented to instantiate a day and time range worked
"""
class DayTimeWorked:
  def __init__(self, day_worked, start_time_worked, end_time_worked):
    self.day_worked = day_worked
    self.start_time_worked = start_time_worked
    self.end_time_worked = end_time_worked

"""
Classes created to implement Iterator Pettern Design
"""
class ScheduleWorkedIterator(Iterator):
  _position: int = None
  _reverse: bool = False

  def __init__(self, collection: ScheduleWorkedCollection, reverse: bool = False) -> None:
    self._collection = collection
    self._reverse = reverse
    self._position = -1 if reverse else 0

  """
  The __next__() method must return the next item in the sequence. On
  reaching the end, and in subsequent calls, it must raise StopIteration.
  """
  def __next__(self):    
    try:
      value = self._collection[self._position]
      self._position += -1 if self._reverse else 1
    except IndexError:
      raise StopIteration()

    return value

"""
Concrete Collections provide one or several methods for retrieving fresh
iterator instances, compatible with the collection class.
"""
class ScheduleWorkedCollection(Iterable):
  
  def __init__(self, collection: List[Any] = []) -> None:
    self._collection = collection

  """
  The __iter__() method returns the iterator object itself, by default we
  return the iterator in ascending order.
  """
  def __iter__(self) -> ScheduleWorkedIterator:
    return ScheduleWorkedIterator(self._collection)

  def get_reverse_iterator(self) -> ScheduleWorkedIterator:
    return ScheduleWorkedIterator(self._collection, True)

  def add_item(self, item: Any):
    self._collection.append(item)