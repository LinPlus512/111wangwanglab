'''
will be used
'''
import os
exit_code = os.system('ping -c 1 8.8.8.8')
print(exit_code)
if exit_code == 0:
    print('Connected success.')
else:
    print('Connected fail')