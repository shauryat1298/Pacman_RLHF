def queryUser(feature_names):
	print "Please enter changes to features in the format:\n(feature 1 number) (+ for increase, - for decrease)\n(feature 2 number) (+/-)\n...\n(enter -1 -1 to stop)"
	for i in range(len(feature_names)):
		print str(i+1)+": "+feature_names[i]
	print "-------------------------------------"
	input_list = []
	for i in range(len(feature_names)):
		input_list.append(None)
	f,sign = raw_input().strip().split(' ')
	f = int(f)
	while (f!=-1):
		input_list[f-1] = sign
		f,sign = raw_input().strip().split(' ')
		f = int(f)

	return input_list

def write_to_file(dict):
	file = open("stored_weights.txt", "w")
	for f in dict:
		file.write(f+" "+str(dict[f])+"\n")
	file.close()

def read_from_file():
	file = open("stored_weights.txt", "r")
	dict = {}
	for line in file.readlines():
		f, val  = line.strip().split()
		dict[f] = float(val)
	file.close()
	return dict

if __name__=="__main__":
	d= {"a" : 3, "b" : 4, "c" : 5, "d" : 7 }
	write_to_file(d)

	print read_from_file()
