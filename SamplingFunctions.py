from sklearn.cluster import KMeans
import numpy as np

def UniformSampling(dset):

	sizes = dset.get_datasets_sizes()

	smallerdset = dset.get_datasets()['small']

	(sizeLarger, sizeSmaller) = (sizes['hasCancer'], sizes['noCancer']) \
									if (sizes['hasCancer'] > sizes['noCancer']) else \
								(sizes['noCancer'],sizes['hasCancer'])

	ratio = int(sizeLarger/sizeSmaller) + 1
	delta = sizeLarger - sizeSmaller * ratio

	for key in smallerdset:
		smallerdset[key] = np.repeat(smallerdset[key], ratio, axis=0)

		#remove rows if necessary
		if delta < 0:
			smallerdset[key] = smallerdset[key][0:delta]

def KMeansSampling(data):

	kmeans = KMeans(n_clusters = 2, random_state = 0).fit(X)
	under_sampling = kmeans.cluster_centers_

def RandomSampling(data):
	pass

def SMOTESampling(data):
	pass
