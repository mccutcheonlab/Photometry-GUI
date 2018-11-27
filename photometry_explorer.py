import scipy.io as sio
import matplotlib.pyplot as plt
import JM_general_functions as jmf


def scale_axis(signal):
    upper = jmf.findpercentilevalue(signal, 0.95)
    lower = jmf.findpercentilevalue(signal, 0.05)
    return [upper, lower]

filename = 'R:\\DA_and_Reward\\es334\\MCP1\\matfiles\\MCP1-1_s1.mat'


a = sio.loadmat(filename, squeeze_me=True, struct_as_record=False)

output = a['output']

blue = output.blue
uv = output.uv

TTLs = []
for x in output._fieldnames:
    var = getattr(output, x)
    if hasattr(var, 'onset'):
        TTLs.append(x)


try:
    fs = output.fs
except:
    fs = output.fs1 



f, ax = plt.subplots(nrows=3, ncols=1, sharex=True)

# Work out TTLs
for i,x in enumerate(TTLs):
    onset = getattr(output, TTLs[0]).onset * fs
    ax[0].scatter(onset, [i]*len(onset))


# Plot blue signal
ax[1].plot(blue, color='blue')
ax[1].set_ylim(scale_axis(blue))

# Plot UV signal
ax[2].plot(uv, color='magenta')
ax[2].set_ylim(scale_axis(uv))


