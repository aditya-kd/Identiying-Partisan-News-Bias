qry_str='this is a happy house'
print('Got This',qry_str)
temp_ls=[]
temp_ls=qry_str.split(' ')
qry_str='%20'.join(temp_ls)
print('Legal Query: ', qry_str)