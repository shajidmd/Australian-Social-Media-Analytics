#!/usr/bin/env python3

import boto
import time

from boto.ec2.regioninfo import RegionInfo
import SettingsFile as info


#----Customizable Info-------------------------------------------
SECS_TO_WAIT = 50

#Instance region and NeCTAR API address
API_ENDPOINT = info.API_ENDPOINT
API_REGION = info.API_REGION

#nectar account test
test_aws_access_key_id= info.test_aws_access_key_id
test_aws_secret_access_key= info.test_aws_secret_access_key
test_key = info.test_key

#nectar account test
test2_aws_access_key_id= "5dd75c367c12461c871d3a305c2671d8"
test2_aws_secret_access_key= "528d33b5262a41d794707ffb412b55aa"
test2_key = info.test_key


#nectar account team
real_aws_access_key_id= info.real_aws_access_key_id
real_aws_secret_access_key= info.real_aws_secret_access_key
real_key = info.real_key


#Instance details
I_TYPE = info.I_TYPE  #Use m2.medium before deploying, instead of m2.tiny
image_name = info.image_name
vol_size = info.vol_size
av_zone = info.av_zone
sec_group= info.sec_group


region = RegionInfo(name=API_REGION, endpoint=API_ENDPOINT)

def connect():
    ec2_conn = boto.connect_ec2(aws_access_key_id=test2_aws_access_key_id, aws_secret_access_key=test2_aws_secret_access_key, is_secure=True, region=region, port=8773, pat$
    return ec2_conn

def listimage(conn):
    #from nectar import ec2_conn
    images = conn.get_all_images()

    for img in images:
        print('Image id: {}, image name: {}'.format(img.id, img.name))

def createInstance(conn):
    instDetails = conn.run_instances(image_name, key_name=test_key, instance_type='m1.small', security_groups=sec_group, placement=av_zone)
    instance = instDetails.instances[0]
    #time.sleep(60)
    #print('New instance {} has been created.'.format(instance.id))
    return instDetails.instances[0].id

def create_vol(conn, vol_size, av_zone):
    new_vol     =       conn.create_volume(vol_size, av_zone)
    return new_vol.id

def attach_vol(conn, volume_id, instance_id, mount_pt):
    conn.attach_volume(volume_id, instance_id, '/dev/vdc')

def show_volume(conn):
    volumes = conn.get_all_volumes()
    for volume in volumes:
        print(volume.status)
        print(volume.zone)
        print(volume.id)

def kill_instance(conn, instance_id):
    conn.terminate_instances(instance_ids=[instance_id])


def showInstances(conn):
    runningInst = conn.get_all_reservations()

    #Show reservation details
    print("The following instances are running: ")
    #for idx, res in enumerate(runningInst, 1):
    #    print(idx, res.id, res.instances)
    print(runningInst[0].instances[0].private_ip_address)

    #Show instance details
    #for idx, runningInst in enumerate(runningInst, 1):
        #print(idx, "---------------")
        #print("IP: ", runningInst.instances[0].private_ip_address)
        #print("Zone: ", runningInst.instances[0].placement)
        #print("id:", runningInst.instances[0].id)
        #print("keyname:", runningInst.instances[0].key_name)

def print_instance_info(inst):
    print()
    print("New instance created with the following details:")
    print("Private IP: ", inst.instances[0].private_ip_address)
    print("Zone: ", inst.instances[0].placement)
    print("ID: ", inst.instances[0].id)
    print("Key: ", inst.instances[0].key_name)
    print()

def update_res_info(conn, instance):

    all_instances = conn.get_all_reservations()
    for inst in all_instances:
        if inst.id == instance.id:
            return inst

def main():
    connection = connect()
    #listimage(connection)
    new_instance = createInstance(connection)
    vol_id= create_vol(connection, vol_size, av_zone)
    show_volume(connection)
    #showInstances(connection)
    #kill_instance(connection, 'i-7e7abe56')
    time.sleep(60)
    showInstances(connection)
    attach_vol(connection, vol_id, new_instance, '/dev/vdc')
    #new_instance = createInstance(connection)
    #time.sleep(SECS_TO_WAIT)
    #print("after sleep")
    #showInstances(connection)

main()
