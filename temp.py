import scipy.io as sio

filename = 'C:\\Users\\James Rig\\Documents\\Tanks\\cTHPH1-04_lick1.mat'

a = sio.loadmat(filename, squeeze_me=True, struct_as_record=False) 
output = a['output']

print(type(output))
