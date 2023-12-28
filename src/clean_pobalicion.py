def clean_pobalicion(data):
    toint = ['relationship_to_hhm', 'sex', 'age', 'type_of_education', 'education', 'education_technical']
    data[toint] = data[toint].astype('int')

    data = data.query('relationship_to_hhm == 1')
    return data
    