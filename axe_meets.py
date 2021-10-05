import numpy as np 
import pandas as pd
import csv

# we'll keep track of who wanted to meet with whom here
interest_list = {}

#let's parse the excel file
with open('axe_meets.csv', newline='') as csvfile:
	reader = csv.reader(csvfile, delimiter=',', quotechar='"')
	next(reader)
	for row in reader:
		interest_list[row[1]] = row[2].split(",")

#let's clean any irregularities in the file
interest_list = {k: [v.strip() for v in vs] for k, vs in interest_list.items()}

# edges = [(a, b) for a, bs in interest_list.items() for b in bs]

# df = pd.DataFrame(edges)

# adj_matrix = pd.crosstab(df[0], df[1])

# print(adj_matrix)

#let's keep track of how many two-way matches each person has
match_list = {}

#let's keep track of who these two way matches are
top_matches = {}
#let's also keep track of one-way matches
secondary_matches = {}

#now let's find all of these two-way and one-way matches
for person, interests in interest_list.items():
	match_list[person] = 0
	top_matches[person] = []
	secondary_matches[person] = []

	for interest in interests:

		if person in interest_list[interest]:
			top_matches[person].append(interest)
			match_list[person] += 1
		else:
			secondary_matches[person].append(interest)

# now we iterate through all of the people
# prioritizing ones that have the lowest number of two way matches
# we put aside the ones with no two way matches for now

have_matches = {key: value for key, value in match_list.items() if value > 0}
no_matches = {key: value for key, value in match_list.items() if value == 0}


prioritized_names = sorted(have_matches, key=lambda k: have_matches[k])

print(prioritized_names)

#now let's begin matching

final_matches = []

completed = {}

#let's keep track of how we're doing in matching
total_two_way_matches = 0
total_one_way_matches = 0
total_non_way_matches = 0

for name in prioritized_names:

	# if we already found a match, don't do anything
	if name in completed:
		continue

	# let's search through the names' two way matches and find if any
	# of them are still available
	for match in top_matches[name]:
		if match in match_list:
			final_matches.append((name,match))
			del match_list[match]
			del match_list[name]
			completed[name] = 1
			completed[match] = 1
			total_two_way_matches += 1
			break

# with the names left over, let's try to find any one-way matches that work
remaining_names = match_list.keys()

for name in remaining_names:
	# if we already found a match, don't do anything
	if name in completed:
		continue

	# let's search through the names' one way matches and find if any
	# of them are still available
	for match in secondary_matches[name]:
		if match in match_list:
			final_matches.append((name,match))
			del match_list[match]
			del match_list[name]
			completed[name] = 1
			completed[match] = 1
			total_one_way_matches += 1
			break

# with the names left over, let's try to find match the rest together
remaining_names = match_list.keys()

def pairwise(iterable):
    a = iter(iterable)
    return zip(a, a)

for x, y in pairwise(remaining_names):
	final_matches.append((name,match))

print(final_matches)

with open('final_matches.csv','w') as out:
    csv_out=csv.writer(out)
    csv_out.writerow(['Name 1','Name 2'])
    for row in final_matches:
        csv_out.writerow(row)




