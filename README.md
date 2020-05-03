# DNS zone file to AWS Terraform file

you can clone the repo and then run 

### % python3 dns2R53.py "the DNS Zone File"

Make sure to convert "@" symbol in the SOA record to be the actual domain name
 
then you may need to delete the NS records before applying the terrafor file.