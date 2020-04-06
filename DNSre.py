import re

fileName = "db.rnstg.com"

Value = re.compile(r'(@)|(\b((?=[a-z0-9-]{1,63}\.)(xn--)?[a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,63}\b)')
Type = re.compile(r'(?<=IN\s)(\w*)')
PointTo = re.compile(r'(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3})|(?<=(\"))(\b.*\b)|((\b((?=[a-z0-9-]{1,63}\.)(xn--)?[a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,63}\b))')

with open (fileName, 'r') as f:
    for line in f:
        try: 
            ValueMatche = Value.search(line).group()
            print(ValueMatche)
            try: 
                TypeMatche = Type.search(line).group()
                print(TypeMatche)
            except: pass
            try: 
                PointToMatches = PointTo.finditer(line)
                for PointToMatche in PointToMatches:
                    if PointToMatche.group() == ValueMatche:
                        pass
                    else:
                        PointToMatche = PointToMatche.group()
                        print(PointToMatche)
                        break
            except: pass
        except: pass
        
     