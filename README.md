# python
zjj's code
1. use case description when to use this script:
	This program is used to achieve a specific account 's summary report of all instances . Include cpu memory net  month / day / year of the maximum | minimum |average datas.
	you will find it very useful to review machine usage based on this report for cost management.
	generate a csv file localy,and csv file's head is 'instance_name','cpu_Average','cpu_Maximum','cpu_Minimum','mem_Average','mem_Maximum','mem_Minimum','NetworkOut_Average','NetworkOut_Maximum','NetworkOut_Minimum','NetworkIn_Average','NetworkIn_Maximum','NetworkIn_Minimum','volumn_VolumeReadOps_Average','volumn_VolumeReadOps_Maximum','volumn_VolumeReadOps_Minimum','volumn_VolumeWriteOps_Average','volumn_VolumeWriteOps_Maximum','volumn_VolumeWriteOps_Minimum'"

2. Prerequisite:
	need ~/.aws/.aws/credentials and need the credentials tag for the different accounts
	best already have the memory cloudwatch metrics  
	need boto3 library 
	need the exact name of the specified tag
	need full access privileges to cloudwatch and ec2

3. Sample input or parameter :
	'-h This program is used to achieve a specific account of all instances (or have a specific label instance) of the cpu memory net Hard disk month / day / year of the maximum | minimum |average summary report,and generate a csv file\n' \
	'-a Account space specified  .aws/credentials tag is used to distinguish between different accounts and space \n '\
	'-p Specify the time interval for the report to support monthly, daily  example：yearly|year|day|month\n '\
	'-t Specify the tag key for resource summary report example：Application|Name|Environment|project\n' \
	'-v Specify tag value for resource summary report example：DMS|SUP|CRM\n' \
	'-r Specify region information  example：cn-north-1\n' \

4. Expected output example:
	[ec2-user@ip-10-208-208-61 tmp]$ python aws_report.py  -r cn-north-1 -v Test-AuthserverTest-env-TY  -t Name -a dev -p month
	tag Name exist !!!! 
	found 1 instance!!!!
	test-authservertest-env-ty CPUUtilization The number of sampling points ---------------1440
	test-authservertest-env-ty CPUUtilization The number of sampling points ---------------1440
	test-authservertest-env-ty CPUUtilization The number of sampling points ---------------1440
	test-authservertest-env-ty MemoryUtilization The number of sampling points ---------------0
	test-authservertest-env-ty MemoryUtilization The number of sampling points ---------------0
	test-authservertest-env-ty MemoryUtilization The number of sampling points ---------------0
	test-authservertest-env-ty NetworkOut The number of sampling points ---------------1440
	test-authservertest-env-ty NetworkOut The number of sampling points ---------------1440
	test-authservertest-env-ty NetworkOut The number of sampling points ---------------1440
	test-authservertest-env-ty NetworkIn The number of sampling points ---------------1440
	test-authservertest-env-ty NetworkIn The number of sampling points ---------------1440
	test-authservertest-env-ty NetworkIn The number of sampling points ---------------1440
	test-authservertest-env-ty VolumeReadOps The number of sampling points ---------------1440
	test-authservertest-env-ty VolumeReadOps The number of sampling points ---------------1440
	test-authservertest-env-ty VolumeReadOps The number of sampling points ---------------1440
	test-authservertest-env-ty VolumeWriteOps The number of sampling points ---------------1440
	test-authservertest-env-ty VolumeWriteOps The number of sampling points ---------------1440
	test-authservertest-env-ty VolumeWriteOps The number of sampling points ---------------1440
	['test-authservertest-env-ty', '0.42%', '4.33%', '0.16%', '0.0%', '0.0%', '0.0%', '10408.33Bytes', '2946074.0Bytes', '5372.0Bytes', '18580.51Bytes', '200111.0Bytes', '10354.0Bytes', ['12.7303240741IOPS', '6729.0IOPS', '0.0IOPS'], ['174.057731481IOPS', '3366.0IOPS', '140.0IOPS']]

5. Error handling or clean-up
	if you don't have MemoryUtilization metrics,report will show 0
	if you imput the wrong account tag ,it will exit 
