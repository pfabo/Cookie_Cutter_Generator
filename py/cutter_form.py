'''
Simple generator for cookie cutters

ver. 0.01 241222
'''

import sys
import cadquery as cq
from cadquery import exporters

if len(sys.argv) < 1:
    print("Use: python cutter_form.py input.dxf ")
    exit()

file_name = sys.argv[1]
stl_name = file_name.split(".")[0] + '.stl'

h1 = 5    # height of the frame
d1 = 3    # frame thickness

hh = [  10,   13,   15,   15]   # cutter wall height
dd = [-2.0, -2.4, -2.8, -3.2]   # extruded retaining walls  

# calculate coordinate origin
vv = (
    cq.importers.importDXF(file_name)
    .val() 
    .CenterOfBoundBox()
)

# outer frame outline
r1 = (
    cq.importers.importDXF(file_name)
    .translate(-vv)
    .wires().toPending()
    .extrude(h1)
)

# inner frame outline
r2 = (
    cq.importers.importDXF(file_name)
    .translate(-vv)
    .wires().toPending()
    .offset2D(-d1)
    .extrude(h1)
)

# cutter
w =[]
for index, value in enumerate(hh): 
    temp = (
        cq.importers.importDXF(file_name)
        .translate(-vv)
        .wires().toPending()
        .offset2D(dd[index])
        .extrude(value)
    )
    w.append(temp)

# final form
r1 = r1.cut(r2)     # ram

for i in range(1, len(hh)-1):
    w[0] = w[0].union(w[i])        
w[0] = w[0].cut(w[-1])

r1 = r1.union(w[0])

# export to *.stl file
exporters.export(r1, stl_name)
exporters.export(r1, 'test.step')




