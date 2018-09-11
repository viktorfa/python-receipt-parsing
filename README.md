# python-receipt-parsing

Project with the goal of creating structured data from (grocery) receipts. Made with [Google Cloud Vision](https://cloud.google.com/vision/) as OCR service in mind. Can theoretically work with any OCR that annotates text in rectangles.

Main focus is being able to extract information about the products bought in a receipt; such as price, description, unit price, quantity, etc...

## Configuration

The project assumes you have an AWS credentials profile called `serverless-admin` in `~/.aws/credentials`.
You need the serverless NPM package to be installed globally `npm i -g serverless`.
You need a Gcloud service credentials json file in `.credentials/gcloud-credentials.json`. It must have a billing account and access to use the Vision API.
For deploying to AWS Lambda, docker must be installed.