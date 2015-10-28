# script to parse the results from M Turk for Tuple Illustrations
import csv
import os
from collections import defaultdict
from string import digits
import json
import pickle # python pickle

config = json.load(open('config.json', 'r'))

output_dir = config['output_dir']
print(os.path.join(output_dir, config['exp_list']))
expms = json.load(open(os.path.join(output_dir, config['exp_list']), 'r'))
try:
    output_file = expms[config['output_file']]
except KeyError:
    print('make sure %s file is updated in %s'%(config['exp_list'],
                                                config['output_dir']))
    sys.exit()

exp_name = output_file.split('.')[0]

with open(os.path.join(output_dir, output_file), 'r') as FILE:
    reader = csv.reader(FILE)

    data = defaultdict(list)

    for i, row in enumerate(reader):
        if i==0 :
            header = row
            # remove approve and reject fields from header
            header.remove('Approve')
            header.remove('Reject')
            # sort header by string value
            head_order = sorted((e, i) for i, e in enumerate(header))
            order = [e for i, e in head_order]
            header = [i for i, e in head_order]
        else:
            # sort the row by the header order
            row = [row[i] for i in order]
            for index, item in enumerate(row):
                # input fileds need to be sorted like strings
                data[header[index].translate(None, digits)].append(item)

inputs = [x for x in data.keys() if 'Input' in x]
answers = [x for x in data.keys() if 'Answer' in x if 'comments' not in x]
# Python 2.7 >
non_out = {k:v for k, v in data.iteritems() if k not in inputs and k not in answers}

# extract non output entries
comments = data['Answer.comments']
# parse to get the results for each input
out = defaultdict(list)
# following code only works when inputs are of length 1 per task

# form a tuple of input values in each row
all_inputs = []

for it in xrange(len(data[inputs[0]])):
    tup = []
    for inp_name in inputs:
        tup.append(data[inp_name][it])
    all_inputs.append(tuple(tup))

for index, inp in enumerate(all_inputs):
    ans_for_in = []
    for ans in answers:
        ans_for_in.append(data[ans][index])
    ans_for_in = tuple(ans_for_in)
    out[inp].append(ans_for_in)

# final out stores the order / meaning of the values in output dict
final_out = {}
final_out['ans_keys'] = tuple(answers)
final_out['data'] = out

# save all the parsed non_out and final_out as jsons
with open(os.path.join(output_dir, exp_name + 'non_out' + '.p'), 'w') as outfile:
    pickle.dump(non_out, outfile)
with open(os.path.join(output_dir, exp_name + 'out' + '.p'), 'w') as outfile:
    pickle.dump(final_out, outfile)
print "Data Parsed Successfully"
