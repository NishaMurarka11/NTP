import xlwt
from xlwt import Workbook
  
# Workbook is created
  

class Metric():

	def addHeaders(self):
		wb = Workbook()
		print("HEADERS")
		# add_sheet is used to create sheet.
		sheet1 = wb.add_sheet('Sheet 1')
		sheet1.write(0, 0, 'Burst_no')
		sheet1.write(0, 1, 'Message_Pair_no')
		sheet1.write(0, 2, 'offset')
		sheet1.write(0, 3, 'delay')
		sheet1.write(0, 4, 'delta')
		sheet1.write(0, 5, 'theta')
		return wb
		


	def populateSheet(self, stats_dict, min_delay_map):
		if stats_dict and min_delay_map:
			lists = stats_dict.items()
			wb = Workbook()
			sheet1 = wb.add_sheet('Sheet 1')
			sheet1.write(0, 0, 'Burst_no')
			sheet1.write(0, 1, 'Message_Pair_no')
			sheet1.write(0, 2, 'offset')
			sheet1.write(0, 3, 'delay')
			sheet1.write(0, 4, 'delta')
			sheet1.write(0, 5, 'theta')
	
		
			burst_msg, y = zip(*lists) # unpack a list of pairs into two tuples
			delay, offset = map(list, zip(*y))
			lists2 = min_delay_map.items()
			x2, y2 = zip(*lists2) # unpack a list of pairs into two tuples
			delta, theta = map(list, zip(*y2))

			sz = len(stats_dict)
			sz2 = len(min_delay_map)
			for i in range(sz):
				burst_no,msg_no = burst_msg[i].split(",")
				sheet1.write(i+1, 0, str(burst_no))
				sheet1.write(i+1, 1, str(msg_no))
				sheet1.write(i+1, 2, str(delay[i]))
				sheet1.write(i+1, 3, str(offset[i]))
				
			ctr = 0
			for i in range(sz2):
				ctr = ctr+8
				sheet1.write(ctr, 4, str(delta[i]))
				sheet1.write(ctr, 5, str(theta[i]))

			wb.save('/Users/illusionist/Desktop/metric.xlsx')


m = Metric()
m.populateSheet(None, None)


