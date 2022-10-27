import mysql.connector as mysql
import regex as re
from regexGen import *
import yaml

dateRegexWithPattern = [
        ['(\d{2}\s*\w{3}\s*\d{4})','%d%b%Y'],
        ['(\d{2}\/\d{1,2}\/\d{4})','%d/%m/%Y'],
        ['(\d{4}-\d{1,2}-\d{2})','%Y-%m-%d'],
        ]

quantityString = [
        'ary',
        'QTY',
        'Quantity',
        ]
db = mysql.connect(
        host="localhost",
        user="lokcharming",
        passwd="asdfasdf",
        database="ERP"
        )

myCursor = db.cursor()
myCursor.execute("select id, name from suppliers")
res = myCursor.fetchall()
allCom = []
supplier_do_num = []
supplier_do_prefix = []
supplier_do_num_regex = []
for row in res:
    temp = []
    temp.append(row[0])
    temp.append(genRegexYaml(row[1]))
    temp.append(row[1])
    allCom.append(temp)

    myCursor.execute("select supplier_do_number from goodsreceiptsnotes where supplier_id="+str(row[0])+" limit 1")
    q = myCursor.fetchall()
    if q:
        supplier_do_num.append(q[0][0])
    else:
        supplier_do_num.append("no record")

for index, i in enumerate(supplier_do_num):
    if i != "no record":
        split = re.split(r'(^[^\d]+)', i)[1:]
        if len(split) != 0:
            #print(split[0])
            supplier_do_prefix.append(split[0])
            print(i)
            print(genRegexWithNum(i))
        else:
            supplier_do_prefix.append('')
        
        if allCom[index][2] == "I-CHAMP TECHNOLOGY PTE LTD":
            supplier_do_num_regex.append("Delivery\s*Number\s*[c,C]*(\d{5})")
        elif allCom[index][2] == "KS PRECISION TOOLS ( JOHOR ) SDN BHD":
            supplier_do_num_regex.append("Delivery\s*[O,0]rder\s*N[o,0].*\s*[:,;,+]*\s*(\d{5})")
        else:
            supplier_do_num_regex.append(genRegexWithNum(i))
    else:
            supplier_do_prefix.append('')
            supplier_do_num_regex.append('')

#print(allCom)
f = open("test.yaml", "w")
f.write("date_format: [\n")
for row in dateRegexWithPattern:
    f.write("   ['")
    f.write(row[0])
    f.write("','")
    f.write(row[1])
    f.write("'],\n")
f.write(']\n\n')

# write Quantity Format
f.write("quantity_format: [\n")
for row in quantityString:
    f.write("   ['")
    f.write(genRegexCapitalInsensitiveAccurate(row))
    f.write("','")
    f.write(row)
    f.write("'],\n")
f.write(']\n\n')
# Write Company
f.write("companies: [\n")
for row in allCom:
    #print(row)
    f.write("[\"")
    f.write(str(row[0]))
    f.write("\",'")
    f.write(row[1])
    f.write("',\"")
    f.write(row[2])
    f.write("\"],\n")
f.write(']\n\n')

# Write company DO regex pattern
for index, row in enumerate(allCom):
    f.write("\"")
    f.write(row[2])
    f.write("\"")
    f.write(':\n')
    f.write('  regex:\n')
    #f.write("      date: ''\n")
    f.write("      do_num: '"+supplier_do_num_regex[index]+"'\n")
    #f.write("      po_num: 'T-*P[O,0,o]-*(\d{8})'\n")
    #f.write("  date_format: ''\n")
    f.write("  do_prefix: '"+supplier_do_prefix[index]+"'\n\n")
     
f.close()

with open('test.yaml', 'r') as file:
    companyYaml = yaml.safe_load(file)

for index, row in enumerate(companyYaml['companies']):
    result = re.search(row[1], row[2])
    if result == None:
        print("GG at ", index)
