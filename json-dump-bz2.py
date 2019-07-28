import json
import bz2
import string
import random

DUMP_FILE_NAME = "lista.dump"
list = []

def random_string(len):
    chars = "".join([random.choice(string.ascii_letters) for i in range(len)])
    return chars

for x in range(0, 1000):
    dict = {"param1": random_string(20), "param2": random_string(20), "param3": random_string(20)}
    list.append(dict)

# open BZ2 file for write with text mode
f = bz2.open(DUMP_FILE_NAME, "wt")
data = json.dumps(list)
f.write(data)
f.close()

# open BZ2 file for read with text mode
f = bz2.open(DUMP_FILE_NAME, "rt")
s = "".join(f.readlines())
list = json.loads(s)
f.close()

print(list)


