#import items
print('__innit__')
import os
import sys
print("Path  :: " ,os.path)
project_path = os.path.dirname( os.path.dirname( os.path.abspath(__file__)))
print(project_path)
project_path = project_path.split('\\')
project_path = '\\'.join(project_path[0:-1])
print(project_path)
sys.path.append(project_path)
