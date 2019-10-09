#
#	Print out a calendar of events 
#	to be scheduled with google calendar
#	in ical format.
#
############################################

import sys, tasks, datetime

#
#	Main
#
def main():

	# import task lists:
	tl = tasks.TaskList(
			sys.argv[1], 
			status=sys.argv[2], 
			subgraph=sys.argv[3]
		)
	tl_time = tasksFromTime(sys.argv[4])

	# print out as calendar:
	beginCalendar()
	printCalEvents(tl, tl_time)
	endCalendar()

#
#	Functions
#
def beginCalendar():
	print(
		'BEGIN:VCALENDAR\n'
		+ 'PRODID:-//K Desktop Environment//NONSGML libkcal 4.3//EN\n'
		+ 'VERSION:2.0\n'
		+ 'X-KDE-ICAL-IMPLEMENTATION-VERSION:1.0\n'
		+ 'X-WR-CALNAME:gantt\n'
		+ 'X-WR-TIMEZONE:Africa/Johannesburg'
	)

def endCalendar():
	print(
		'END:VCALENDAR'
	)

def printCalEvents(tasklist, tasklist_time):
	i = 0	# index for task list
	j = 0	# index for graph nodes
	k = 0	# index for subgraphs

	# create path stack:
	pathstack = [tasklist.infile[:-4]]

	while i < len(tasklist.tasks)-1:
		il = tasklist.getIndentLevel(i)
		il_next = tasklist.getIndentLevel(i+1)
		if il<il_next:
			pathstack.append(tasklist.tasks[i][tasklist.maxIndent])
			k+=1
		elif il==il_next:
			printAsEvent(tasklist, i, pathstack, tasklist_time, j)
			j+=1
		else:
			printAsEvent(tasklist, i, pathstack, tasklist_time, j)
			del pathstack[-1]
			j+=1
		i+=1
	printAsEvent(tasklist, i, pathstack, tasklist_time, j)	

def printAsEvent(tasklist, taskindex, path, tasklist_time, taskindex_time):
	desc = '/'
	for x in path:
		desc += x + '/'
	tasklabel=tasklist.tasks[taskindex][tasklist.maxIndent]
	dur = tasklist_time[taskindex_time][2]
	relstart = int(tasklist_time[taskindex_time][3])
	printEvent(desc+tasklabel,'',relstart,dur)

def printEvent(summary,description,relstart,duration):
	# find next monday:
	d = datetime.datetime.today()
	next_monday = next_weekday(d, 0)

	start = next_monday + datetime.timedelta(weeks=(relstart-1))

	print('BEGIN:VEVENT')
	print('SUMMARY:'+summary)
	print(
		'DTSTART;VALUE=DATE:'
		+str(start.year)
		+format(start.month, '02d')
		+format(start.day, '02d')
	)
	print('DURATION:'+duration)
	print('TRANSP:TRANSPARENT')
	print('DESCRIPTION:'+description)
	print('END:VEVENT')

def next_weekday(d, weekday):
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0: # Target day already happened this week
        days_ahead += 7
    return d + datetime.timedelta(days_ahead)

def tasksFromTime(timeFile):
	tasks = []
	# open time file:
	instream = open(sys.argv[4], 'r')
	while True:
		rawline = instream.readline().strip()
		# skip over empty lines:
		if not rawline:
			continue
		if rawline[0].isdigit():
			taskindex = int(rawline.split(" ")[0])
			tasklabel = instream.readline().strip()[20:-10]
			taskdur   = instream.readline().strip()[8:-5]
			taskend   = instream.readline().strip()[4:-5]
			if taskdur == '-':
				taskdur = 'P1D'
			else:
				taskdur = 'P'+taskdur+'W'
			task = [taskindex, tasklabel, taskdur, taskend]
			tasks += [task]

		if rawline.find('/* Edges */') != -1:
			break

	instream.close()

	return tasks

#
#	Boilerplate
#
if __name__ == "__main__":
	main()