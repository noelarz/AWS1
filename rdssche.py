import boto3
import datetime
import time
import os
import pprint

rds = boto3.client('rds')
os.environ['TZ'] = 'America/New_York'
pp = pprint.PrettyPrinter(indent=4)

def lambda_handler(event, context):
    ts = time.time()
    DayOfWeek = datetime.datetime.fromtimestamp(ts).strftime('%w')
    HourOfDay = datetime.datetime.fromtimestamp(ts).strftime('%-H')
    MinuteOfDay = datetime.datetime.fromtimestamp(ts).strftime('%M')
    print("DayOfWeek=%s,HourOfDay=%s,MinuteOfDay=%s" % (DayOfWeek,HourOfDay,MinuteOfDay))
    
    dbs = rds.describe_db_instances()
    for db in dbs['DBInstances']:
        db_id = db['DBInstanceIdentifier']
        db_name = db['DBName']
        db_all = dbs['DBInstances']
        db_arn = db['DBInstanceArn']
        db_status = db['DBInstanceStatus']
        print db_id
        print db_name
        print db_status
        print db_arn
        #print db_all
        tags = rds.list_tags_for_resource(ResourceName=db_arn)
        #print tags
        #print tags['TagList'][0]['Key']
        off = ""
        on = ""
        Name = ""
        days = ""
        leaveon = ""
        leaveoff = ""
        for num in range(0, len(tags['TagList'])):
            if tags['TagList'][num]['Key'] == 'Name':
                Name = tags['TagList'][num]['Value']
                print Name
            if tags['TagList'][num]['Key'] == 'days':
                days = tags['TagList'][num]['Value']
                print days
            if tags['TagList'][num]['Key'] == 'on':
                on = tags['TagList'][num]['Value']
                print on
            if tags['TagList'][num]['Key'] == 'off':
                off = tags['TagList'][num]['Value']
                print off
            if tags['TagList'][num]['Key'] == 'leaveoff':
                leaveoff = tags['TagList'][num]['Value']
                print leaveoff
            if tags['TagList'][num]['Key'] == 'leaveon':
                leaveon = tags['TagList'][num]['Value']
                print leaveon
        
        onminute = ""
        offminute = ""
        onhour = ""
        offhour = ""
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
                        pp.pprint(rds.start_db_instance(DBInstanceIdentifier=db_id))
                    else:
                        leaveon = int(leaveon)
                        leaveon = leaveon-1
                        leaveon = str(leaveon)
                        rds.add_tags_to_resource(
                                ResourceName=db_arn,
                                Tags=[
                                    {
                                        'Key': 'leaveon',
                                        'Value': leaveon,
                                    },
                                ],
                            )
                        print leaveon
        if ( HourOfDay == offhour ):
                if (MinuteOfDay == offminute ):
                        if ( leaveoff == "0" ) or ( leaveoff == ""):
                            pp.pprint(rds.stop_db_instance(DBInstanceIdentifier=db_id))
                            print "more stuff"
                        else:
                            leaveoff = int(leaveoff)
                            leaveoff = leaveoff-1
                            leaveoff = str(leaveoff)
                            rds.add_tags_to_resource(
                                ResourceName=db_arn,
                                Tags=[
                                    {
                                        'Key': 'leaveoff',
                                        'Value': leaveoff,
                                    },
                                ],
                            )
                            
                            
                            print leaveoff
