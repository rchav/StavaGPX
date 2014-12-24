import pandas as pd

filename = '20130223-233104-Ride.gpx'

points =[]
recordID = []
count = 0

with open(filename, 'r') as file:
	for line in file:
		cleanLine = line.strip()
		if cleanLine[:6] == "<trkpt":
			points.append(line)
			count = count + 1
			recordID.append(count)

df = pd.DataFrame(columns = ['Record', 'Trackpoint', 'Lat', 'Long', 'Elevation', 'Date'])
df['Record'] = recordID
df['Trackpoint'] = points

print df
