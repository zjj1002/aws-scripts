# -*- coding:utf-8 -*-  
import boto3
import getopt
import sys
 
 
def usage():
    print ' -h help 本程序用于批量生成邮件报警 报警接受者可以订阅sns消息\n' \
          ' -a metric to set 把需要设置报警的metric作为参数 需要准确 \n' \
          ' -t threshold 把对应metric的阀值设在这里\n' \
          " -u unit 把对应metric的计量单位设在这里 Unit='Seconds'|'Microseconds'|'Milliseconds'|'Bytes'|'Kilobytes'|'Megabytes'|'Gigabytes'|'Terabytes'|'Bits'|'Kilobits'|'Megabits'|'Gigabits'|'Terabits'|'Percent'|'Count'|'Bytes/Second'|'Kilobytes/Second'|'Megabytes/Second'|'Gigabytes/Second'|'Terabytes/Second'|'Bits/Second'|'Kilobits/Second'|'Megabits/Second'|'Gigabits/Second'|'Terabits/Second'|'Count/Second'|'None'\n" \
          " -n namespaces are reserved for use by Amazon Web Services products 具体要加哪个方面的报警设在这里 如果监控的是aws的自己服务 请参看http://docs.aws.amazon.com/zh_cn/AmazonCloudWatch/latest/monitoring/aws-namespaces.html 如果是AWS提供的自定义监控请使用System/Linux作为namesapce  例子： namespace='AWS/ECS'|'AWS/EC2'|'AWS/Lambda'|'AWS/Redshift'|'AWS/S3'|'AWS/EBS'|''System/Linux\n"

def put_alarm(AlarmType,Threshold,Unit,INSTANCES):
    if INSTANCES:
        for INSTANCE_ID in INSTANCES:
            cloudwatch.put_metric_alarm(
                AlarmName='Server_%s_%s_Utilization'%(AlarmType,INSTANCE_ID),
                ComparisonOperator='GreaterThanThreshold',
                EvaluationPeriods=1,
                MetricName=AlarmType,
                Namespace=namespace,
                Period=300,
                Statistic='Average',
                Threshold=float(Threshold),
                ActionsEnabled=True,
                AlarmActions=['arn:aws-cn:sns:cn-north-1:407271452911:cloudwatch_notification'],
                AlarmDescription='Alarm when server %s exceeds %s'%(AlarmType,Threshold)+'%',
                Dimensions=[
                {
                  'Name': 'InstanceId',
                  'Value': INSTANCE_ID
                },
                ],
                Unit=Unit
                )
            print "============  added alarm for %s Server_%s_%s_Utilization !!!======================" % (INSTANCE_ID,AlarmType,INSTANCE_ID)
    else:
        print "==============  can't find any INSTANCES relate to this AlarmType  ==================="
        return 0

def get_all_metrics(AlarmType,namespace):
    instances = []
    Namespace = namespace
    response = cloudwatch.list_metrics(
        Namespace = Namespace,
        MetricName=AlarmType,
    )
    for i in response['Metrics']:
        for k in i[u'Dimensions']:
            if k['Name'] == 'InstanceId':
                instances.append(k['Value'])
    return instances

if __name__ == '__main__':
    if ( len( sys.argv ) < 9 ):
        print 'please -h or --help for detail'
        usage()
        sys.exit(1)
    try:
        options, args = getopt.getopt(sys.argv[1:], "ha:t:u:n:", ['help', "alarm=", "threshold=","Unit=","namespace="])
        for name, value in options:
            if name in ('-h', '--help'):
                usage()
            elif name in ('-a', '--alarm'):
                AlarmType = value
            elif name in ('-t', '--threshold'):
                Threshold = value
            elif name in ('-u', '--unit'):
                Unit = value
            elif name in ('-n', '--namespace'):
                namespace = value
    except getopt.GetoptError:
        usage()
# Create CloudWatch client
    cloudwatch = boto3.client('cloudwatch',region_name='cn-north-1')
    ins = get_all_metrics(AlarmType,namespace)
    put_alarm(AlarmType,Threshold,Unit,ins)
