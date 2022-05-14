import boto3
import subprocess
ec2 = boto3.resource('ec2')
 
# Create a new EC2 instance 
instances = ec2.create_instances(
     ImageId='ami-09d56f8956ab235b3',
     MinCount=1,
     MaxCount=1,
     InstanceType='t2.micro',
     KeyName='devops'
 )

#ssh into machine


#run bash script to install wp on instance created

subprocess.call("installwp.sh")