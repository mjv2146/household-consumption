def clean(data):
    toint = ['location_size']
    data[toint] = data[toint].astype('int')
    return data