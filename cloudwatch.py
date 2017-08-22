# -*- coding:utf-8 -*-  
import boto3
import getopt
import sys
 
 
def usage():
    print ' -h help 本程序用于批量生成邮件报警 报警接受者可以订阅sns消息\n' \
          ' -a metric to set 把需要设置报警的metric作为参数 需要准确 \n' \
          ' -t threshold 把对应metric的阀值设在这里\n' \
          " -u unit 把对应metric的计量单位设在这里 Unit='Seconds'|'Microseconds'|'Milliseconds'|'Bytes'|'Kilobytes'|'Megabytes'|'Gigabytes'|'Terabytes'|'Bits'|'Kilobits'|'Megabits'|'Gigabits'|'Terabits'|'Percent'|'Count'|'Bytes/Second'|'Kilobytes/Second'|'Megabytes/Second'|'Gigabytes/Second'|'Terabytes/Second'|'Bits/Second'|'Kilobits/Second'|'Megabits/Second'|'Gigabits/Second'|'Terabits/Second'|'Count/Second'|'None' "

def put_alarm(AlarmType,Threshold,Unit,INSTANCE_ID):
    cloudwatch.put_metric_alarm(
        AlarmName='Server_%s_Utilization'%AlarmType,
        ComparisonOperator='GreaterThanThreshold',
        EvaluationPeriods=1,
        MetricName=AlarmType,
        Namespace='AWS/EC2',
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

def get_all_metrics():
    instances = []
    response = cloudwatch.list_metrics(
        Namespace='AWS/EC2',
        MetricName='CPUUtilization',
    )
    for i in response['Metrics']:
        for k in i[u'Dimensions']:
            if k['Name'] == 'InstanceId':
                instances.append(k['Value'])
    return instances

if __name__ == '__main__':
    if ( len( sys.argv ) < 6 ):
        print 'please -h or --help for detail'
        usage()
        sys.exit(1)
    try:
        options, args = getopt.getopt(sys.argv[1:], "ha:t:u:", ['help', "alarm=", "threshold=","Unit="])
        for name, value in options:
            if name in ('-h', '--help'):
                usage()
            elif name in ('-a', '--alarm'):
                AlarmType = value
            elif name in ('-t', '--threshold'):
                Threshold = value
            elif name in ('-u', '--unit'):
                Unit = value
    except getopt.GetoptError:
        usage()
# Create CloudWatch client
    cloudwatch = boto3.client('cloudwatch',region_name='cn-north-1')
    ins = get_all_metrics()
    put_alarm(AlarmType,Threshold,Unit,ins[1])
