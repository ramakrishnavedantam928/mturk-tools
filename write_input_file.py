import os
import csv
import json
import pickle
import numpy as np
import sys

def process_imname(path, name):
    return -1

config = json.load(open('config.json', 'r'))
path_to_data = '../data/hit_data'
path_to_images = 'https://filebox.ece.vt.edu/~vrama91/visualw2v/data/pr_image_data/'
# for pilot
num_per_hit = 5
primitives = ['id', 'img']
seed = 124
# uncomment for pilot
#input_file_name = 'pilot.csv'
# uncomment to launch final task
input_file_name = 'final.csv'

# load data and have a random access order
np.random.seed(seed)
data = pickle.load(open(os.path.join(path_to_data,'pr_data.p') ,'r'))
select_inputs = range(260, len(data))
perm = np.random.permutation(len(data))[select_inputs]
print('Creating %d HITs' % (len(perm)/num_per_hit))

input_file = os.path.join(path_to_data, input_file_name)
FILE = open(input_file, 'w')
csvwriter = csv.writer(FILE, delimiter=',')

try:
    assert(len(perm)/float(num_per_hit) == len(perm)/num_per_hit)
except:
    print('Make sure the number of HITs per file and number of tasks are divisible')
    sys.exit()

header = []
for i in xrange(1,num_per_hit+1):
    for p in primitives:
        header.append(p + str(i))

# write header to the csv file
csvwriter.writerow(header)

# permute the data

data_ptr = 0
for row in xrange(len(perm)/num_per_hit):
    write_row = []
    for col in xrange(num_per_hit):
        image_path = os.path.join(path_to_images, data[perm[data_ptr]][-1])
        image_id = data[perm[data_ptr]][-1].split('.')[0]
        write_row.append(image_id)
        write_row.append(image_path)
        data_ptr += 1
    csvwriter.writerow(write_row)

FILE.close()
