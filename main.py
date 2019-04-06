import csv
import pybullet as pb
from convexify import create_urdf_file
from ycb_downloader import download_files

def object_list():

    reject_list = ['N/A1', 'N/A2', 'N/A3', '3', '2']

    objects_to_download = []

    with open('object_list.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for i, row in enumerate(csv_reader):
            if i == 0:
                continue
            if row[1] == 'Processed (.tgz)':
                objects_to_download.append(row[0])

    return objects_to_download


def test_urdf(urdf_root_path):
    pb.connect(pb.GUI)
    pb.loadURDF(urdf_root_path)
    while  True:
        pb.stepSimulation()
        

ycb_output_directory = "./ycb"

urdf_output_directory = "./models"

# You can either set this to "all" or a list of the objects that you'd like to
# download.
#objects_to_download = "all"
#objects_to_download = ["002_master_chef_can", "003_cracker_box"]
# objects_to_download = ["003_cracker_box Processed"]

# You can edit this list to only download certain kinds of files.
# 'berkeley_rgbd' contains all of the depth maps and images from the Carmines.
# 'berkeley_rgb_highres' contains all of the high-res images from the Canon cameras.
# 'berkeley_processed' contains all of the segmented point clouds and textured meshes.
# 'google_16k' contains google meshes with 16k vertices.
# 'google_64k' contains google meshes with 64k vertices.
# 'google_512k' contains google meshes with 512k vertices.
# See the website for more details.
#files_to_download = ["berkeley_rgbd", "berkeley_rgb_highres", "berkeley_processed", "google_16k", "google_64k", "google_512k"]
files_to_download = ["berkeley_processed"]

objects_to_download = object_list()

test_object = False

for obj in objects_to_download:


    print "Dowloading object %s"%obj

    download_files(objects_to_download=[obj], 
                   files_to_download=files_to_download,  
                   output_directory=ycb_output_directory, 
                   extract=True)


    print "Generating URDF of the object object %s"%obj

    urdf_root_path = create_urdf_file(output_directory=urdf_output_directory, 
                                     input_mesh=ycb_output_directory+('/%s/%s')%(obj,'tsdf/nontextured.stl'))

    print "URDF stored at %s"%urdf_root_path

    if test_object:

        test_urdf(urdf_root_path=urdf_root_path)