import re
import sys

if len(sys.argv) < 2:
    print("Usage:\n{0} <zonefile>".format(sys.argv[0]))
    exit(1)

def _gen_zone(**d):
    return """
resource "aws_route53_zone" "{root_zone_name}" {{
  name = "{root_zone}"
}}""".format(
        **d
    )


def _gen_record(**d):
    return """
resource "aws_route53_record" "{record_name}" {{
  zone_id = aws_route53_zone.{root_zone_name}.zone_id
  name    = "{name}"
  type    = "{type}"
  records = ["{record}"]
  ttl     = {ttl}
}}""".format(
        **d
    )

fileName = sys.argv[1]
TTL = "3600"

Value = re.compile(r"(@)|((\b|\*.)((?=[a-z0-9-_]{1,63}\.)(xn--)?[a-z0-9_\*]+(-[a-z0-9]+)*\.)+[a-z]{2,63}\b)|(^\w*\b)")
Type = re.compile(r"(?<=IN\s)(\w*)|([Mm][Xx])|([Ss][Rr][Vv])")
PointTo = re.compile(r"(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3})|(?<=(\"))(\b.*\b)|((\b((?=[a-z0-9-]{1,63}\.)(xn--)?[a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,63}\b))")
Priority = re.compile(r"(?<=[Mm][Xx]\s)(\d*)|(?<=[Ss][Rr][Vv]\s)(\d*)")
Port_Or_Weight = re.compile(r"(\b\d{1,5}\b)")

with open (fileName, 'r') as f:
    root_zone = ""
    root_zone_name = ""
    for line in f:
        try: 
            ValueMatche = Value.search(line).group()
            # print(ValueMatche)
            try: 
                TypeMatche = Type.search(line).group()
                # print(TypeMatche)
            except: pass
            try: 
                PointToMatches = PointTo.finditer(line)
                for PointToMatche in PointToMatches:
                    if PointToMatche.group() == ValueMatche:
                        pass
                    else:
                        PointToMatche = PointToMatche.group()
                        # print(PointToMatche)
                        break
            except: pass
            try:
                PriorityMatch = Priority.search(line).group()
            except:
               pass
            try:
                Port_Or_Weight_Match = Port_Or_Weight.finditer(line)
                next(Port_Or_Weight_Match)
                Port = next(Port_Or_Weight_Match).group()
                Weight = next(Port_Or_Weight_Match).group()
            except: pass
            if TypeMatche == "SOA":
                root_zone = ValueMatche
                root_zone_name = root_zone.replace('.','_')

                print (_gen_zone(root_zone=root_zone,
                        root_zone_name=root_zone_name))
            
            elif TypeMatche == "A" or TypeMatche == "CNAME" or TypeMatche == "TXT":
                print (_gen_record(record_name='{0}-{1}'.format(ValueMatche.replace('.','_').replace('*','_'),PointToMatche.lower().replace('.','_').replace('=','_').replace('+','_').replace(':','_').replace(' ', '')),
                    name=ValueMatche,
                    ttl=TTL,
                    type=TypeMatche,
                    record=PointToMatche,
                    root_zone_name=root_zone_name))
            elif TypeMatche == "MX":
                PointToMatche_MX = f'{PriorityMatch} {PointToMatche}'
                print (_gen_record(record_name='{0}-{1}'.format(ValueMatche.replace('.','_'),PointToMatche.lower().replace('.','_')),
                    name=ValueMatche,
                    ttl=TTL,
                    type=TypeMatche,
                    record=PointToMatche_MX,
                    root_zone_name=root_zone_name))
            elif TypeMatche == "SRV":
                PointToMatche_SRV = f'{PriorityMatch} {Weight} {Port} {PointToMatche}'
                print (_gen_record(record_name='{0}-{1}'.format(ValueMatche.replace('.','_'),PointToMatche.lower().replace('.','_')),
                    name=ValueMatche,
                    ttl=TTL,
                    type=TypeMatche,
                    record=PointToMatche_SRV,
                    root_zone_name=root_zone_name))
            else:
                print (_gen_record(record_name='{0}-{1}'.format(ValueMatche.replace('.','_'),PointToMatche.lower().replace('.','_')),
                    name=ValueMatche,
                    ttl=TTL,
                    type=TypeMatche,
                    record=PointToMatche,
                    root_zone_name=root_zone_name))
        except: pass