import re

fileName = "db.rnstg.com"
TTL = "3600"

Value = re.compile(r'(@)|(\b((?=[a-z0-9-]{1,63}\.)(xn--)?[a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,63}\b)')
Type = re.compile(r'(?<=IN\s)(\w*)')
PointTo = re.compile(r'(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3})|(?<=(\"))(\b.*\b)|((\b((?=[a-z0-9-]{1,63}\.)(xn--)?[a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,63}\b))')

with open (fileName, 'r') as f:
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
            # print (f'{ValueMatche}\t{TypeMatche}\t{PointToMatche}')

            print (
                f"resource" "aws_route53_record" "support_aa-dining_com" "{"
                    "zone_id" "=" "aws_route53_zone.aa-dining_com.zone_id"
                    "name" "=" "support.aa-dining.com"
                    "type" "=" "CNAME"
                    "ttl"  "=" "3600"
                    "records" "=" "[""aa-dining.zendesk.com""]"
                "}"
            )








        except: pass



# resourceName = 
# zone_id = aws_route53_{resourceName}.zone_id
# name = "{ValueMatche}"
# RTtype = "{TypeMatche}"
# records = "{PointToMatche}"
# ttl = "{TTL}"





# resource "aws_route53_zone" "aa-dining_com" {
#   name = "aa-dining.com"
#   tags = {"Name":"aa-dining.com", "DNS":"External", "Resource":"DNS"}
#   comment = "Managed by TF"
# }

# resource "aws_route53_record" "support_aa-dining_com" {
#   zone_id = aws_route53_zone.aa-dining_com.zone_id
#   name    = "support.aa-dining.com"
#   type    = "CNAME"
#   ttl     = "3600"
#   records = ["aa-dining.zendesk.com"]
# }
