import os
import numpy as np
from PIL import Image

def crop_image(path, witdh, height):
	offset_h = 10
	for root, dirs, files in os.walk(path, True):
		for name in files:
			image = Image.open(os.path.join(root, name))
			w, h = image.size
			offset_w = (w - witdh) / 2
			image.crop((0 + offset_w, 0 + offset_h, witdh + offset_w, height + offset_h)).save(os.path.join(root, name))

def convert_to_grayscale(path):
	for root, dirs, files in os.walk(path, True):
		for name in files:
			image = Image.open(os.path.join(root, name))
			image.convert('L').save(os.path.join(root, name))

def rename_filename(filename, operation_flag=1):
	# type: 1 sequence
	# type: 2 image
	if operation_flag == 1:
		end_position = 8
	elif operation_flag == 2 : 
		end_position = 17
	else:
		print "Illegal rename type. Default to sequence type."
		end_position = 8
	return filename[:end_position]

def search_label_dictionary(label_dict, filename, operation_flag=1):
	name = rename_filename(filename, operation_flag)
 	for index, value in label_dict:
 		if index == name:
 			return value

def generate_label_dictionary(path, operation_flag=1):
	label = []
	for root, dirs, files in os.walk(path, True):
		for name in files:
			f = open(os.path.join(root, name), 'r')
			label.append([rename_filename(name, operation_flag), int(float(f.read()))])
	return label

def set_record_size(label, witdh, height, channel):
	return label + (witdh * height * channel)

def generate_bin(path, total_images, record_size, label_dict, home_path):
	result = np.empty([total_images, record_size], dtype=np.uint8)
	i = 0
	label_found = []
	for root, dirs, files in os.walk(path, True):
		for name in files:
			label = search_label_dictionary(label_dict, name)
			if label is not None:
				print "Label found was: " + str(label)
				#label_found.append(label)
				image = Image.open(os.path.join(root, name))
				image_modifed = np.array(image)
				grey = image_modifed[:].flatten()
				result[i] = np.array(list([label]) + list(grey), np.uint8)
				i = i + 1
			else:
				print "Label was not found for :" + name
	result.tofile(home_path)
	#unique_label = set(label_found)
	#print unique_label

def main(argv=None):  # pylint: disable=unused-argument
	label_path = "/home/neo/projects/deepLearning/data/label/"
	#image_path = "/home/neo/projects/deepLearning/data/image/"
	image_path = "/home/neo/projects/deepLearning/data/resize_faces_seq_10/"
	home_path = "/home/neo/projects/deepLearning/data/ck_24.bin"
	#total_images = 4895
	#total_images = 327
	total_images = 3064
	#witdh = 640
	#height = 480
	witdh = 64
	height = 64
	channel = 1
	label = 1
	operation = 1
	#convert_to_grayscale(image_path)
	#label_dict = generate_label_dictionary(label_path, operation)
	record_size = set_record_size(label, witdh, height, channel)
	print record_size
	#generate_bin(image_path, total_images, record_size, label_dict, home_path)

	
if __name__ == '__main__':
	main()