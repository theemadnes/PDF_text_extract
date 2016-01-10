# Overview

This code, written to be executed as an AWS Lambda function, uses the Slate module to extract the text from a PDF file, and then indexes that text to an ElasticSearch cluster. It is designed to be invoked when a PDF document is put to an S3 bucket.
