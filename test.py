import datetime

#print(end_date - end_date)
begin_date = datetime.datetime.strptime('2015-02-20 00:00:00',"%Y-%m-%d %H:%M:%S")
end_date = datetime.datetime.strptime('2015-02-27 00:00:00',"%Y-%m-%d %H:%M:%S")
Interval_date = end_date-begin_date
print((end_date-begin_date).days)
