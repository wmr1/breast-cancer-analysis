from keras.layers import Dense
from keras.layers import Dropout
from keras.models import Sequential
from keras.regularizers import l2, l1
from keras.callbacks import EarlyStopping
from Util import *

from sklearn.metrics import roc_curve, recall_score, precision_score, f1_score
from sklearn.metrics import accuracy_score, roc_auc_score, confusion_matrix

import numpy as np

import matplotlib.pyplot as plt

class NeuralNetworkGenerator:

	architectures = []
	architectures_scores = []

	def __init__(self, path, epochs = 150, batch_size = 64):
		self.path = path
		self.epochs = epochs
		self.batch_size =  batch_size

		with open(path, "r") as f:
			qtd_archs = f.readline()
			for _ in range(0, int(qtd_archs)):
				activation, regularization = f.readline().split(" ")
				layers = f.readline().split(" ")
				self.architectures.append({'regularization' : float(regularization),
										   'activation' : activation.replace('\n', ''),
				                           'layers' : list(map(int, layers))
				                           })

	def evaluate(self, dataset):
		x = 1
		np.random.seed(7)

		for arch in self.architectures:
			model = Sequential()

			for i in range(len(arch['layers'])):
				if i == 0:
					model.add(Dense(arch['layers'][i+1], input_dim = arch['layers'][i], activation = arch['activation']))
					i += 1
				elif i < len(arch['layers']) - 1:
					
					model.add(Dense(arch['layers'][i], activation=arch['activation'], activity_regularizer=l2(arch['regularization'])))

				else:
					model.add(Dense(arch['layers'][i], activation = 'sigmoid'))

			# Compile model.
			model.compile(loss = 'binary_crossentropy', optimizer = 'adam', metrics = ['accuracy'])

			# Get dataset variables.
			dset = dataset.get_dataset()

			# Fit the model.
			history = model.fit(dset['X_train'], dset['y_train'], epochs = self.epochs, batch_size = self.batch_size,
			                    callbacks = [EarlyStopping(patience = 50)], validation_data = (dset['X_val'], dset['y_val']))

			# Evaluate the model.
			scores = model.evaluate(dset['X_test'], dset['y_test'])
			#self.architectures_scores.append((scores, len(history.history['loss'])))

			y_pred = model.predict(dset['X_test'])
			y_pred_class = model.predict_classes(dset['X_test'], verbose = 0)

			plot_training_error_curves(history)
			plot_roc_curve(dset['y_test'], y_pred)


			losses = extract_final_losses(history)

			print()

			print('Confusion matrix:')
			print(confusion_matrix(dset['y_test'], y_pred_class))
			print("{metric:<18}{value:.4f}".format(metric = "Train Loss:", value = losses['train_loss']))
			print("{metric:<18}{value:.4f}".format(metric = "Validation Loss:", value = losses['val_loss']))
			print("{metric:<18}{value:.4f}".format(metric = "Test Loss:", value = scores[0]))
			print("{metric:<18}{value:.4f}".format(metric = "Accuracy:", value = accuracy_score(dset['y_test'], y_pred_class)))
			print("{metric:<18}{value:.4f}".format(metric = "Recall:", value = recall_score(dset['y_test'], y_pred_class)))
			print("{metric:<18}{value:.4f}".format(metric = "Precision:", value = precision_score(dset['y_test'], y_pred_class)))
			print("{metric:<18}{value:.4f}".format(metric = "F1:", value = f1_score(dset['y_test'], y_pred_class)))
			print("{metric:<18}{value:.4f}".format(metric = "AUROC:", value = roc_auc_score(dset['y_test'], y_pred)))

			x += 1

		#self.store_test_scores()

	def store_test_scores(self):
		i = 1
		print("Storing test scores...")
		with open("results/output.txt", "w") as f:
			for scores in self.architectures_scores:
				f.write("\nArchitecture %d \n%s: %.2f%% (%d)" % (i, "accuracy", scores[0][1] * 100, scores[1]))
				i += 1
