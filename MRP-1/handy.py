 ### Imports ###
import os,sys,errno

 ### Handy functions ###

# Everything needs to be rewritten so that this function does not have to be used.
def specify_loc ():
	print ""
	telescope_loc = raw_input ("LaSilla or LaPalma:                        " )
	print ""
	return telescope_loc

# Converts hours to hours and minutes, for example: 20.25 ---> 20h 15m. Also rounds a bit.
def h2hm(h):
	i = 0
	while True:
		if h > 1: i += 1; h-= 1
		else: break
	m = int(round(h*60,0))
	return '{0:02}h {1:02}m'.format(i,m)

# Shows a progressbar.
def progress (value,endvalue,bar_length=20):
	percent = float(value)/endvalue
	arrow = '-'*int(round(percent*bar_length)-1)+'>'
	spaces = ' '*(bar_length-len(arrow))
	sys.stdout.write('\r[{0}] {1}%'.format(arrow+spaces,int(round(percent*100))))
	sys.stdout.flush() # Is only useful to use if nothing else on the screen is printed.

# Computes the date of tomorrow.
def next_date(year,month,day,skip): 
	# TODO: Implement that the skip only works if specified which station is used. So make an extra variable called station=LP (station=LS).
	if day == 28 and month == 2:
		month += 1;day = 1
	elif day == 30 and ( month == 4 or month == 6 or month == 9 or month == 11 ):
		month += 1; day = 1
	elif day == 31 and ( month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 ):
		month += 1; day = 1
	elif day == 31 and month == 12:
		year += 1; month = 1; day = 1
	elif day == 28 and month == 12 and year == 2017 and skip == True: # Because there are no lightcurve folders for the 29th FOR LASILLA.
		day += 2
	else: day += 1
	
	return year,month,day

# Creates an array with all the observation days wanted.
def observation_dates(start_date,end_date,skip): 
	ob_array = []
	cur_date = start_date # type: string.
			
	year = int(cur_date[0])*1000+int(cur_date[1])*100+int(cur_date[2])*10+int(cur_date[3])*1
	month = int(cur_date[4])*10+int(cur_date[5])*1
	day = int(cur_date[6])*10+int(cur_date[7])*1

	while True:
		if month >= 10 and day < 10: ob_array.append(str(year)+str(month)+'0'+str(day))
		elif month < 10 and day >= 10: ob_array.append(str(year)+'0'+str(month)+str(day))
		elif day < 10 and month < 10: ob_array.append(str(year)+'0'+str(month)+'0'+str(day))
		else: ob_array.append(str(year)+str(month)+str(day))
		if ob_array[len(ob_array)-1]==end_date:
			break
			
		year,month,day = next_date(year,month,day,skip)
	
	return ob_array

# Prints strings in both the terminal and a text file.
def double_printer(s, text_file):
	sys.stdout.write('{0}'.format(s))
	text_file.write('{0}'.format(s))

# Makes a directory given a path.
def mk_dir(dir_name):
	try: os.makedirs(dir_name)
	except OSError as sys.exit:
		if sys.exit.errno != errno.EEXIST: raise

# Adds input elements to an array and returns it.
def add_to_array(array,string):
	while True:
		if len(array)==0:
			entry = raw_input(string)
		else: entry = raw_input('                                           ')
		if entry.lower () == '':
			break
		array.append(entry)
	return array

def ra_conversion(h,m,s):
	return str(h*15.0+m*(15.0/60.0)+s*(15.0/3600.0))

def dec_conversion(d,m,s):
	return str(d+m/60.0+s/(3600.0))