import pandas

icelollies = pandas.DataFrame({'name': ['Fab', 'Twister', 'Rocket'], 'packet_size': ['6', '5', '5']})
icelollies['packet_size_int'] = pandas.to_numeric(icelollies.packet_size)
print(icelollies.dtypes)