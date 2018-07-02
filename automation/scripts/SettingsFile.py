#!/usr/bin/env python3

#Settings enabling access to CCC team's NeCTAR account


#----Customizable Info-------------------------------------------
SECS_TO_WAIT = 50

#Instance region and NeCTAR API address
API_ENDPOINT = 'nova.rc.nectar.org.au'
API_REGION = 'melbourne'

#nectar account test
test_aws_access_key_id='86ea212bfdea4e418275c5e04e5b25cd'
test_aws_secret_access_key='8f9cd81fa3cc4eeabd1ade5c5bd1d188'
test_key = 'demokey'

#nectar account team
real_aws_access_key_id='3a94a61c5ed64c2982946622b5cba9ef'
real_aws_secret_access_key='0ca6142fd31d4ba98529227fd6d5c63e'
real_key = 'cloudkey'


#Instance details
I_TYPE = 'm2.medium'  #Use m2.medium before deploying, instead of m2.tiny
image_name = 'ami-000022b3'
vol_size = 5
av_zone = 'melbourne-np'
sec_group=['default']
