# Overview

This code, written to be executed as an AWS Lambda function, uses the Slate module to extract the text from a PDF file, and then indexes that text to an ElasticSearch cluster. It is designed to be invoked when a PDF document is put to an S3 bucket.


A few implementation notes:
* Play around with the Lambda timeout time to set something that works for document sizes you're placing in the S3 bucket
* This assumes some familiarity with AWS Lambda basics (configuring events sources, invocation policies, etc)
* Specify a suffix of 'pdf' to make sure it's only executing for pdf files