import csv_lab, math

PARTITION = 5
file_num = 1
csv_path = 'bus8.csv'

new_path_pre = 'final'
new_path_suf = '.csv'

csv_list = csv_lab.csv_to_list(csv_path)
header = csv_list[0]
csv_len = len(csv_list) - 1

'''
example. csv = [1,1,1,1], divide into 3
len(csv)

'''
partition_len = csv_len // PARTITION

print "partition size %d" % partition_len
print "Original len: %d" % csv_len

for i in range(PARTITION):
	new_path = new_path_pre + str(file_num) + new_path_suf
	new = [header[:]]
	beg = partition_len * i + 1
	end = partition_len * (i+1) + 1
	if file_num == PARTITION:
		new += csv_list[beg:]
	else:
		new += csv_list[beg:end]

	csv_lab.write_list_to_csv(new, new_path)

	print "File %d len: %d" % (file_num, len(new))

	file_num += 1
