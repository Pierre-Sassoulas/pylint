value1 = 'test'
value2 = 'Add ' + value1 + ' to other value'  # [consider-using-f-string]
value3 = 0
value4 = ''
value4 += 'Add ' + str(value3) + ' to yet other value'  # [consider-using-f-string]
