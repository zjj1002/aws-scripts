# -*- coding: UTF-8 -*-
import sys
import os
import boto3
import datetime
import csv
import getopt

def usage():
	print '-h This program is used to achieve a specific account of all instances (or have a specific label instance) of the cpu memory net Hard disk month / day / year of the maximum | minimum |average summary report,and generate a csv file\n' \
              '-a Account space specified  .aws/credentials tag is used to distinguish between different accounts and space \n '\
              '-p Specify the time interval for the report to support monthly, daily  example：yearly|year|day|month\n '\
	      '-t Specify the tag key for resource summary report example：Application|Name|Environment|project\n' \
	      '-v Specify tag value for resource summary report example：DMS|SUP|CRM\n' \
	      '-r Specify region information  example：cn-north-1\n' \
	      ''
def get_all_instanceid(tag="",tagvalue=""):
	dict_info = {}
	ebs_info = {}
	count = 0
	if tag:
		response = ec2.describe_tags(DryRun=False,MaxResults=123,)
		for i in response['Tags']:
			if i['Key'] == tag and i['Value'] == tagvalue:
				instances = ec2.describe_instances(Filters=[{'Name': 'instance-state-name', 'Values': ['running']},{'Name':'tag-key', 'Values':[tag]},{'Name':'tag-value', 'Values':[tagvalue]}])
				print "tag %s exist !!!! " % tag
				break
	else:
		instances = ec2.describe_instances(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
	for instance in instances['Reservations']:
		for i in  instance['Instances']:
			for j  in  i['Tags']:
				if j['Key'] == 'Name':
					dict_info[j['Value'].lower()] = i['InstanceId']
					count = count + 1
			dict_info[i['InstanceId']]= []
			for volume in i['BlockDeviceMappings']:
				dict_info[i['InstanceId']].append(volume['Ebs']['VolumeId']) 
	print "found %d instance!!!!" % count
	return dict_info
def write_report(period,tag="",tagvalue=""):
	dict_info = get_all_instanceid(tag,tagvalue)
	if period == 'month':
		time_delta = 30
		time_period = 1800
	elif period == 'day':
		time_delta = 1
		time_period = 60
	elif period == 'year':
		time_delta = 365
		time_period = 21900
	for key,value in dict_info.items():
		collection = []
		if type(value) is not list:
			collection.append(key) 
			collection.extend([get_metrics('InstanceId',value,key,'CPUUtilization',time_delta,'Percent',time_period,statistic,'AWS/EC2') for statistic in ('Average','Maximum','Minimum')])
			collection.extend([get_metrics('InstanceId',value,key,'MemoryUtilization',time_delta,'Percent',time_period,statistic,'System/Linux') for statistic in ('Average','Maximum','Minimum')])
			collection.extend([get_metrics('InstanceId',value,key,'NetworkOut',time_delta,'Bytes',time_period,statistic,'AWS/EC2') for statistic in ('Average','Maximum','Minimum')])
			collection.extend([get_metrics('InstanceId',value,key,'NetworkIn',time_delta,'Bytes',time_period,statistic,'AWS/EC2') for statistic in ('Average','Maximum','Minimum')])
			for volumn_id in dict_info[value]:
				collection.append([get_metrics('VolumeId',volumn_id,key,'VolumeReadOps',time_delta,'Count',time_period,statistic,'AWS/EBS') for statistic in ('Average','Maximum','Minimum')])
				collection.append([get_metrics('VolumeId',volumn_id,key,'VolumeWriteOps',time_delta,'Count',time_period,statistic,'AWS/EBS') for statistic in ('Average','Maximum','Minimum')])
			print collection
			writer.writerow(collection)


def get_metrics(search_name,instance_id,instance_name,metric,time_delta,unit,period,statistic,namespace):
	try:
		result = 0.0
		count = 0
		sum_result = 0.0
		metric_data = cloudwatch.get_metric_statistics(Namespace=namespace,MetricName=metric,Dimensions=[{'Name': search_name,'Value': instance_id},],StartTime=datetime.datetime.utcnow() - datetime.timedelta(days=time_delta),EndTime=datetime.datetime.utcnow(),Period=period,Statistics=[statistic,],Unit=unit)['Datapoints']
		for i in metric_data:
			#print metric,instance_name,i
			if 	statistic == 'Average':
					sum_result = i[statistic] + sum_result 		
			elif	statistic == 'Maximum':
					result = max(result,i[statistic])
			elif	statistic == 'Minimum' and count == 0:
					result = i[statistic]
			elif	statistic == 'Minimum' and count > 0: 
					result = min(result,i[statistic])
			count = count + 1
		if statistic == 'Average' and count != 0:
			metric_data = sum_result / count
		else:
			metric_data = result
		print "%s %s The number of sampling points ---------------%d" % (instance_name,metric,count)
		if unit == "Percent":
			return str(round(metric_data,2)) + "%"
		elif unit == "Bytes":
			return str(round(metric_data,2)) + "Bytes"
		elif unit == "Count":
			return str(metric_data) + "IOPS"
		else:	
			return metric_data
	except IndexError,e:
		#print instance_name +"	"+"missing  %s customize metrics!!!!" % metric 
		return 0.0	

if __name__ == '__main__':
	if ( len( sys.argv ) < 11 ):
		print 'please -h or --help for detail'
        	usage()
        	sys.exit(1)
	try:
        	options, args = getopt.getopt(sys.argv[1:], "ha:a:p:t:v:r:", ['help','tagvalue=', 'account=','period=','tag=','region='])
        	for name, value in options:
            		if name in ('-h', '--help'):
                		usage()
            		elif name in ('-a', '--account'):
                		account = value
			elif name in ('-p', '--period'):
                                period = value
				if period not in ('month,year,day'):
					usage()
					sys.exit(1)
			elif name in ('-t', '--tag'):
				tag = value
			elif name in ('-v', '--tagvalue'):
				tagvalue = value
			elif name in ('-r', '--region'):
				region = value
    	except getopt.GetoptError:
        	usage()
	reload(sys)
	sys.setdefaultencoding( "utf-8" )
	try:
		session = boto3.Session(profile_name = account)
	except:
		print "there is no account for %s" % account
		sys.exit()
	ec2 = session.client('ec2', region_name='cn-north-1')
	cloudwatch = session.client('cloudwatch', region_name=region)
	csvfile = open('report.csv', 'wb')
	writer = csv.writer(csvfile)
	writer.writerow(['instance_name', 'cpu_Average', 'cpu_Maximum','cpu_Minimum','mem_Average','mem_Maximum','mem_Minimum','NetworkOut_Average','NetworkOut_Maximum','NetworkOut_Minimum','NetworkIn_Average','NetworkIn_Maximum','NetworkIn_Minimum','volumn_VolumeReadOps_Average','volumn_VolumeReadOps_Maximum','volumn_VolumeReadOps_Minimum','volumn_VolumeWriteOps_Average','volumn_VolumeWriteOps_Maximum','volumn_VolumeWriteOps_Minimum',])
	write_report(period,tag,tagvalue)
