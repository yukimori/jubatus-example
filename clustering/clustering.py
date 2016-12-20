# coding: utf-8

from __future__ import print_function
import jubatus
from jubatus.common import Datum

datasets_name = ["noisy_circles", "noisy_moons", "blobs"]
datasets_directory = "./datasets/"

datasets = {}
for name in datasets_name:
    dataset = []
    with open(datasets_directory+name+".dat", "r") as f:
        for line in f:
            cluster, x, y, = line.rstrip().split(",")
            dataset.append({"x":float(x), "y":float(y), "cluster": int(cluster)})
    datasets[name] = dataset

print("loaded three datasets(./datasets/{{{0[0]},{0[1]},{0[2]}}}.csv). Each dataset has two cluster. See ./expect/{{{0[0]},{0[1]},{0[2]}}}.png".format(datasets_name))

host = '127.0.0.1'
port = 9199
name = 'test'

client = jubatus.Clustering(host, port, name)

print("excute clustering the datasets")

for name, dataset in datasets.items():
    client.clear()

    print("======")
    print("start to push {0} data with id(execute clustering {1} times)".format(name, client.get_revision()))
    for i, data in enumerate(dataset):
        client.push([( str(i) , Datum({"x" : data['x'], "y" : data['y']}))])
    print("{0} data pushed(calculate cluster : {1} times)".format(len(dataset), client.get_revision()))
    
    clusters = client.get_core_members_light()
    print("get cluster info. it has {0} clusters".format(len(clusters)))
    for i, cluster in enumerate(clusters):
        print("{0} cluster include {1} data".format(str(i+1), len(cluster)))
        print("    id:[", end='')
        for point in cluster:
            print("{0}".format(point.id), end=' ')
        print("]")
    print("")

