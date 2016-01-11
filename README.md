# Overview

This code, written to be executed as an AWS Lambda function, uses the Slate module to extract the text from a PDF file, and then indexes that text to an ElasticSearch cluster. It is designed to be invoked when a PDF document is put to an S3 bucket.


A few implementation notes:
* Because this is just a simple PoC, the only text data index to Elasticsearch is on the first page 
* Play around with the Lambda timeout time to set something that works for document sizes you're placing in the S3 bucket
* For smaller PDF docs, I've observed memory utilization (in CWL) of low 10s of Mbytes
* This assumes some familiarity with AWS Lambda basics (configuring events sources, invocation policies, etc)
* Specify a suffix of 'pdf' to make sure it's only executing for pdf files

To be implemented:
* Signing of POSTs to Elasticsearch endpoints using SigV4, instead of using python modules 