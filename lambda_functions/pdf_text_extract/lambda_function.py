from __future__ import print_function

import json
import urllib
import boto3
import slate # using a specific version of PDFminer due to incompatibilities of certain versions
import elasticsearch
import datetime

es_endpoint = 'search-mattsona-pdf-repo-2vzllafnl4d5oeu647oyu6yy6i.us-west-2.es.amazonaws.com'
es_index = 'pdf_text_extracts'
es_type = 'document'

print('Loading function')

s3 = boto3.client('s3')

# prepare a dict to hold our document data
doc_data = {}
doc_data['insert_time'] = str(datetime.datetime.isoformat(datetime.datetime.now()))


def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))

    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    object_key = urllib.unquote_plus(event['Records'][0]['s3']['object']['key']).decode('utf8')
    try:
        # get the file data from s3
        temp_pdf_file = open('/tmp/tempfile.pdf', 'w') # create a file handler for the temporary file
        response = s3.get_object(Bucket=bucket, Key=object_key)
        print("CONTENT TYPE: " + response['ContentType'])
        # return response['ContentType']
        temp_pdf_file.write(response['Body'].read()) # write the object data to a local file; will be passed to slate
        temp_pdf_file.close() # close the temporary file for now

        # pull the text from the temporary PDF file using slate
        print("Extracting data from: " + object_key)
        with open('/tmp/tempfile.pdf') as temp_pdf_file:

            doc = slate.PDF(temp_pdf_file)

        # store document data to dict
        doc_data['source_pdf_name'] = object_key
        doc_data['document_text'] = doc[0] # we're only worried about page 1 at this point

    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(object_key, bucket))
        raise e

    # put the data in ES
    try:
        es = elasticsearch.Elasticsearch([{'host': es_endpoint, 'port': 443, 'use_ssl': True}]) # hold off on validating certs
        es_response = es.index(index=es_index, doc_type=es_type, body=doc_data)
        print('Data posted to ES: ' + str(es_response))

    except Exception as e:
        print('Data post to ES failed: ' + str(e))
        raise e   

    return "Done"
