import os
import csv
import sys
from PIL import Image
import numpy as np

from utils import load_csv, check_distribution, check_cumulative_distribution

dataset = "dataset"
archive = "archive"
test = "test"
train = "train"
good = "good"
not_good = "not-good"
np_txt = "np_text"

csv_path = "csv"
csv_dir_good = "good.csv"
csv_dir_not_good = "not_good.csv"

cwd_parent = os.path.dirname(os.getcwd())
test_dir = os.path.join(os.path.abspath(cwd_parent), dataset, archive, test)
train_good_dir = os.path.join(os.path.abspath(cwd_parent), dataset, archive, train, good)
train_not_good_dir = os.path.join(os.path.abspath(cwd_parent), dataset, archive, train, not_good)

csv_train_good_dir = os.path.join(os.path.abspath(cwd_parent), dataset, archive, csv_path, csv_dir_good)
csv_train_not_good_dir = os.path.join(os.path.abspath(cwd_parent), dataset, archive, csv_path, csv_dir_not_good)

def countSamples():
    # 180 test samples
    # 250 good samples
    # 50 not-good samples

    count = 0
    for path in os.listdir(train_not_good_dir):
        if os.path.isfile(os.path.join(train_not_good_dir, path)):
            count += 1
    
    print("test_dir has this many samples: ", count)

def define_anomaly():
    anomaly_dict = {}
    for filename in os.listdir(train_not_good_dir):
        #emove file extension
        name, ext = os.path.splitext(filename)
        # remove number
        name = ''.join([i for i in name if not i.isdigit()])

        if name in anomaly_dict:
            anomaly_dict[name] += 1

        else:
            anomaly_dict[name] = 1
    
    print(anomaly_dict)

    # {'manipulated_front': 10, 'scratch_head': 10, 'scratch_neck': 10, 'thread_side': 10, 'thread_top': 10}

def create_file_list(scrape_dir, format = '.png'):
    fileList = []
    print(scrape_dir)

    for root, dirs, files in os.walk(scrape_dir, topdown=False):
        for name in files:
            if name.endswith(format):
                fullName = os.path.join(root, name)
                fileList.append(fullName)
    
    return fileList

def convert_data_to_csv(folder, label):
    # label 0 = anomaly, 1 = normal

    file_list = create_file_list(folder)
    # np_collect = []

    for file in file_list:
        print(file)
        img_file = Image.open(file)
        # img_file.show()

        # get original image parameters...
        width, height = img_file.size
        format = img_file.format
        mode = img_file.mode

        # make image Greyscale
        img_grey = img_file.convert('L')


        # Save Greyscale values
        value = np.asarray(img_grey.getdata(), dtype=np.int).reshape((img_grey.size[1], img_grey.size[0]))
        value = value.flatten()
        # value = np.append(label, value)
        print(value)

        # add current image to np_collect
        # if len(np_collect) == 0:
        #     np_collect = value

        
        # np_collect = np.vstack([np_collect, value])

        
        # save csv
        with open("test.csv", 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(value)

    # np.savetxt("not_good_txt", np_collect, delimiter=" ")


if __name__ == "__main__":
    print("this is analyze")
    # countSamples()
    # define_anomaly()
    # convert_data_to_csv(test_dir, 1)
    data = load_csv(csv_train_good_dir, True)
    # check_distribution(data)
    check_cumulative_distribution(data)