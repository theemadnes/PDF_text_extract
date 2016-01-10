from __future__ import print_function

import json
import urllib
import boto3
import slate
import elasticsearch

elasticsearch_endpoint = ''

print('Loading function')

s3 = boto3.client('s3')


def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))

    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.unquote_plus(event['Records'][0]['s3']['object']['key']).decode('utf8')
    try:
        # get the file data from s3
        temp_pdf_file = open('tempfile.pdf', 'w') # create a file handler for the temporary file
        response = s3.get_object(Bucket=bucket, Key=key)
        print("CONTENT TYPE: " + response['ContentType'])
        # return response['ContentType']
        temp_pdf_file.write(response['Body'].read()) # write the object data to a local file; will be passed to slate
        temp_pdf_file.close() # close the temporary file for now

        # pull the text from the temporary PDF file using slate
        with open('tempfile.pdf') as temp_pdf_file:

            doc = slate.PDF(temp_pdf_file)

        return "Done."

    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e

