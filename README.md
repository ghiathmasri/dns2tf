# DNS zone file to AWS Terraform file

you can clone the repo and then run 

python3 DNSre.py <the DNS Zone File> > <the name of terraformfile for output>.tf 
  OR
python3 DNSre.py <the DNS Zone File>
  if you want to see the results in the terminal

  
then you may need to delete the NS records before applying the terrafor file.
