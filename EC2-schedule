import boto3
import datetime
import time
import os
import pprint

ec = boto3.client('ec2')
os.environ['TZ'] = 'America/Chicago'
pp = pprint.PrettyPrinter(indent=4)

def lambda_handler(event, context):

    ts = time.time()

    DayOfWeek = datetime.datetime.fromtimestamp(ts).strftime('%w')
    HourOfDay = datetime.datetime.fromtimestamp(ts).strftime('%-H')
    MinuteOfDay = datetime.datetime.fromtimestamp(ts).strftime('%M')
    
    print("DayOfWeek=%s,HourOfDay=%s,MinuteOfDay=%s" % (DayOfWeek,HourOfDay,MinuteOfDay))

    reservations = ec.describe_instances(
        Filters=[
            {'Name': 'tag-key', 'Values': ['days', 'Days']},
        ]
    ).get(
        'Reservations', []
        
    )
    instances = sum(
        [
            [i for i in r['Instances']]
            for r in reservations
        ], [])
        
    for instance in instances:
        off = ""
        on = ""
        Name = ""
        days = ""
        leaveon = ""
        leaveoff = ""
        for tag in instance['Tags']:
            if tag['Key'] == 'Name':
                Name = tag['Value']
            if tag['Key'] == 'days':
                days = tag['Value']
            if tag['Key'] == 'on':
                on = tag['Value']
            if tag['Key'] == 'off':
                off = tag['Value']
            if tag['Key'] == 'leaveon':
                leaveon = tag['Value']
            if tag['Key'] == 'leaveoff':
                leaveoff = tag['Value']
        print("Name=%s,off=%s(%s:%s),on=%s(%s:%s),days=%s(%s),leaveon=%s,leaveoff=%s" % (Name,off,HourOfDay,MinuteOfDay,on,HourOfDay,MinuteOfDay,days,DayOfWeek,leaveon,leaveoff))
        if ( DayOfWeek in days ):
###### START OF EXECUTING ON/OFF/DAYS CODE
            onminute = ""
            offminute = ""
            onhour = ""
            offhour = ""
            instanceId = [instance['InstanceId']]
            if (on):
                on = on.replace('-',':')
                on = on.replace(':','')
                onhour = str(int(on[:-2]))
                onminute = on[-2:]
            if (off):
                off = off.replace('-',':')
                off = off.replace(':','')
                offhour = str(int(off[:-2]))
                offminute = off[-2:]
            if ( HourOfDay == onhour ):
            	if ( MinuteOfDay == onminute ):
                    if ( leaveon == "0" ) or ( leaveon == ""):
                        try:
                            pp.pprint(ec.start_instances(InstanceIds=instanceId))
                        except:
                            print "Instance start problem!!"
                    else:
                        leaveon = int(leaveon)
                        leaveon = leaveon-1
                        leaveon = str(leaveon)
                        ec.create_tags(Resources=instanceId, Tags=[{'Key':'leaveon', 'Value':leaveon}])
                        print leaveon
            if ( HourOfDay == offhour ):
                if (MinuteOfDay == offminute ):
                        if ( leaveoff == "0" ) or ( leaveoff == ""):
                            try: 
                                pp.pprint(ec.stop_instances(InstanceIds=instanceId))
                            except:
                                print "Instance stop problem!!!"
                        else:
                            leaveoff = int(leaveoff)
                            leaveoff = leaveoff-1
                            leaveoff = str(leaveoff)
                            ec.create_tags(Resources=instanceId, Tags=[{'Key':'leaveoff', 'Value':leaveoff}])
                            print leaveoff
