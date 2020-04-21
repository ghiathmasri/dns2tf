# DNS zone file to AWS Terraform file

you can clone the repo and then run 

### % python3 DNSre.py "the DNS Zone File" > "the name of terraformfile for output".tf 
  ## OR
#### % python3 DNSre.py "the DNS Zone File"

If you want to see the results in the terminal

Make sure to convert "@" symbol in the SOA record to be the actual domain name
 
then you may need to delete the NS records before applying the terrafor file.
