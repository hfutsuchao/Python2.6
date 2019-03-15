#coding:utf-8
#!/usr/bin/python
fc = open('./cartOrderData','r').readlines()
fu = open('./newUser','r').readlines()
fo = open('./orderPaid','r').readlines()

dicOrderUsers = {}
dicOrderCreateUsers = {}
dicUserNew = {}
dicOrderCreateUsersNew = {}
dicOrderUsersNew = {}
dicOrderPaid = {}
dicOrderPaidNew = {}

for line in fu:
	created_time, user_id = line.split('\t')
	dicUserNew[created_time] = user_id

for line in fc:
    created_time, ca_name, user_id, order_code, item_settings = line.split('\t')
    if created_time not in dicOrderCreateUsers:
    	dicOrderCreateUsers[created_time] = []
    	dicOrderUsers[created_time] = []
        dicOrderPaid[created_time] = []
        dicOrderPaidNew[created_time] = []
    if item_settings.find('"rentPrice":0') == -1:
        dicOrderUsers[created_time].append(user_id)
    if order_code:
    	dicOrderCreateUsers[created_time].append(user_id)
for line in fo:
    created_time, user_id = line.split('\t')
    dicOrderPaid[created_time].append(user_id)

for created_time in dicOrderCreateUsers:
    dicOrderCreateUsersNew[created_time] = [i for i in dicOrderCreateUsers[created_time] if i>=dicUserNew[created_time]]
    dicOrderUsersNew[created_time] = [i for i in dicOrderUsers[created_time] if i>=dicUserNew[created_time]]
    dicOrderPaidNew[created_time] = [i for i in dicOrderPaid[created_time] if i>=dicUserNew[created_time]]

#AllUser's date OrderUV OrderPV OrderCreateUV OrderCreatePV OrderPaid
for created_time in sorted(dicOrderCreateUsers):
	print created_time + '\t' + str(len(set(dicOrderUsers[created_time]))) + '\t' + str(len(dicOrderUsers[created_time])) + '\t' + str(len(set(dicOrderCreateUsers[created_time]))) + '\t' + str(len(dicOrderCreateUsers[created_time])) + '\t' + str(len(set(dicOrderPaid[created_time])))

print '\n'

#newUser's date OrderUV OrderPV OrderCreateUV OrderCreatePV OrderPaid
for created_time in sorted(dicOrderCreateUsers):
    print created_time + '\t' + str(len(set(dicOrderUsersNew[created_time]))) + '\t' + str(len(dicOrderUsersNew[created_time])) + '\t' + str(len(set(dicOrderCreateUsersNew[created_time]))) + '\t' + str(len(dicOrderCreateUsersNew[created_time])) + '\t' + str(len(set(dicOrderPaidNew[created_time])))
