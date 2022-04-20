import crhelper
import boto3

# initialise logger
logger = crhelper.log_config({"RequestId": "INIT"})
logger.info('Logging configured')
# set global to track init failures
init_failed = False

try:
    #Initialise 
    logger.info("Initialization completed")
except Exception as e:
    logger.error(e, exc_info=True)
    init_failed = e

def create(event, context):
    logger.info("Creating directory")
    s3 = boto3.client('s3')
    b=event['ResourceProperties']['bucket']
    f=event['ResourceProperties']['directory']
    s3.put_object(Bucket=b, Key=(f+'/'))
    physical_resource_id = f
    response_data = {}
    return physical_resource_id, response_data

def update(event, context):
    logger.info("Updating bucket with new directory")
    s3 = boto3.client('s3')
    b=event['ResourceProperties']['bucket']
    f=event['ResourceProperties']['directory']
    s3.put_object(Bucket=b, Key=(f+'/'))
    physical_resource_id = f
    response_data = {}
    return physical_resource_id, response_data

def delete(event, context):
    logger.info("Deleting directory")
    s3 = boto3.client('s3')
    b=event['ResourceProperties']['bucket']
    f=event['ResourceProperties']['directory']
    s3.delete_object(Bucket=b,Key=(f+'/'))
    return

def lambda_handler(event, context):
    # update the logger with event info
    global logger
    logger = crhelper.log_config(event)
    return crhelper.cfn_handler(event, context, create, create, delete, logger,
                                init_failed)

