# -*- coding: utf-8 -*-

f = open("breast.db",'r')
x = open("breast.txt",'w')
counter = 0
first = True
for line in f.readlines():
    if counter > 5:
        curr = line.split()
        s = ''
        for i in range(1,len(curr)-2):
            s += str(curr[i]) + " ";
        s += curr[len(curr)-1]
        if first:
            x.write(s)
            first = False
        else:
            x.write("\n"+s);
        counter += 1
    else:
        counter += 1
print(str(counter))