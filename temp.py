import scipy.io as sio

filename = 'R:\\DA_and_Reward\\es334\\MCP1\\matfiles\\MCP1-1_s1.mat'


a = sio.loadmat(filename, squeeze_me=True, struct_as_record=False)

output = a['output']

