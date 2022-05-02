#!python
# convert triangulations between leapfrog and vulcan
# input_path: a file or a wildcard with files to be converted
# output_path: (optional) if blank a file with same base name will be saved
'''
usage: $0 input_path*00t,msh,obj,xlsx output_path*00t,msh,csv,obj,xlsx
'''

import sys, os.path
import pandas as pd
import time
import re
import glob


# import modules from a pyz (zip) file with same name as scripts
sys.path.insert(0, os.path.splitext(sys.argv[0])[0] + '.pyz')

from _gui import usage_gui, leapfrog_load_mesh, leapfrog_save_mesh, wavefront_load_obj, wavefront_save_obj, df_to_nodes_faces, nodes_faces_to_df, pd_save_dataframe, pd_load_dataframe
from vulcan_save_tri import vulcan_save_tri, vulcan_load_tri

def tri_leapfrog_convert(input_path, output_path = None):
  print("# tri_leapfrog_convert")
  if not output_path:
    output_path = os.path.splitext(input_path)[0]
    if input_path.lower().endswith('00t'):
      output_path += '.msh'
    else:
      output_path += '.00t'

  c = time.time()
  nodes = None
  faces = None
  if input_path.endswith('00t'):
    nodes, faces, cv, cn = vulcan_load_tri(input_path)
  elif input_path.endswith('msh'):
    nodes, faces = leapfrog_load_mesh(input_path)
  elif input_path.endswith('obj'):
    od = wavefront_load_obj(input_path)
    nodes = od.get('v')
    faces = od.get('f')
  else:
    df = pd_load_dataframe(input_path)
    nodes, faces = df_to_nodes_faces(df)

  print(len(nodes),"nodes", len(faces),"faces time=", time.time() - c)
  if output_path.endswith('csv'):
    import csv
    with open(output_path, 'w', newline='') as csvfile:
      csvwriter = csv.writer(csvfile)
      csvwriter.writerow(['#','nodes',str(len(nodes))])
      csvwriter.writerows(nodes)
      csvwriter.writerow(['#','faces',str(len(faces))])
      csvwriter.writerows(faces)
  elif output_path.endswith('00t'):
    vulcan_save_tri(nodes, faces, output_path)
  elif output_path.endswith('msh'):
    leapfrog_save_mesh(nodes, faces, output_path)
  elif output_path.endswith('obj'):
    wavefront_save_obj(output_path, {'v': nodes, 'f': faces})
  else:
    df = nodes_faces_to_df(nodes, faces)
    pd_save_dataframe(df, output_path)

  print("# tri_leapfrog_convert total",time.time() - c)

# main
def main(input_path, output_path):
  if '*' in input_path:
    for f in glob.glob(input_path):
      tri_leapfrog_convert(f)
  else:
    tri_leapfrog_convert(input_path, output_path)


if __name__=="__main__": 
  usage_gui(__doc__)
