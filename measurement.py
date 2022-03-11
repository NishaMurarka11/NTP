import xlwt
from xlwt import Workbook
  
# Workbook is created
wb = Workbook()
  
# add_sheet is used to create sheet.
sheet1 = wb.add_sheet('Sheet 1')
  
sheet1.write(0, 0, 'Burst_no')
sheet1.write(0, 1, 'Message_Pair_no')
sheet1.write(0, 2, 'offset')
sheet1.write(0, 3, 'delay')
sheet1.write(0, 4, 'delta')
sheet1.write(0, 5, 'theta')
  

class Metric():
	
	def populateSheet(stats_dict, min_delay_map):
		wb = Workbook()
		sheet1 = wb.add_sheet('Sheet 1')
		burst_msg, y = zip(*lists) # unpack a list of pairs into two tuples
		delay, offset = map(list, zip(*y))
		x2, y2 = zip(*lists2) # unpack a list of pairs into two tuples
		delta, theta = map(list, zip(*y2))

		sz = len(stats_dict)
		for i in range(sz):
			burst_no,msg_no = burst_msg[i].split(",")
			sheet1.write(i+1, 0, burst_no)
			sheet1.write(i+1, 1, msg_no)
			sheet1.write(i+1, 2, delay[i])
			sheet1.write(i+1, 3, offset[i])
			sheet1.write(i+1, 4, delta[i])
			sheet1.write(i+1, 5, theta[i])

		wb.save('/Users/illusionist/Desktop/metric.xlsx')



