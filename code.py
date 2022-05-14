import boto3
ec2 = boto3.resource('ec2')

# create VPC and subnet
vpc = ec2.create_vpc(CidrBlock='192.168.0.1/16')

#name vpc

vpc.create_tags(Tags=[{"Key": "Fiifi_vpc", "Value": vpc.id}])

vpc.wait_until_available()

# enable public dns hostname so that we can SSH into it later
ec2Client = boto3.client('ec2')
ec2Client.modify_vpc_attribute( VpcId = vpc.id , EnableDnsSupport = { 'Value': True } )
ec2Client.modify_vpc_attribute( VpcId = vpc.id , EnableDnsHostnames = { 'Value': True } )


# create an internet gateway and attach it to VPC
internetgateway = ec2.create_internet_gateway()
vpc.attach_internet_gateway(InternetGatewayId=internetgateway.id)

# create a route table and a public route
routetable = vpc.create_route_table()
route = routetable.create_route(DestinationCidrBlock='0.0.0.0/0', GatewayId=internetgateway.id)

# create subnet and associate it with route table
subnet = ec2.create_subnet(CidrBlock='172.16.1.0/24', VpcId=vpc.id)
routetable.associate_with_subnet(SubnetId=subnet.id)

securitygroup = ec2.create_security_group(GroupName='SSH-ONLY', Description='only allow SSH traffic', VpcId=vpc.id)
securitygroup.authorize_ingress(CidrIp='0.0.0.0/0', IpProtocol='tcp', FromPort=22, ToPort=22)


# create a file to store the key locally
outfile = open('ec2-keypair.pem', 'w')

# call the boto ec2 function to create a key pair
key_pair = ec2.create_key_pair(KeyName='ec2-keypair')

# capture the key and store it in a file
KeyPairOut = str(key_pair.key_material)
outfile.write(KeyPairOut)

# Create a linux instance in the subnet
instances = ec2.create_instances(
 ImageId='ami-0de53d8956e8dcf80',
 InstanceType='t2.micro',
 MaxCount=1,
 MinCount=1,
 NetworkInterfaces=[{
 'SubnetId': subnet.id,
 'DeviceIndex': 0,
 'AssociatePublicIpAddress': True,
 'Groups': [securitygroup.group_id]
 }],
 KeyName='ec2-keypair')

 #change key of the ssh key with this command:  chmod 400 ec2-keypair.pem
