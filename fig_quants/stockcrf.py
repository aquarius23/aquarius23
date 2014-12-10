#!/usr/bin/python
#!coding=utf-8
import crfsuite

# Inherit crfsuite.Trainer to implement message() function, which receives
# progress messages from a training process.
class crftrainer(crfsuite.Trainer):
	def message(self, s):
		print s

class stockcrftrainer():
	# Create a Trainer object.
	trainer = crftrainer()

	def clear(self):
		self.trainer.clear()

	def set_tag_feature(self, tags, features):
		xseq = crfsuite.ItemSequence()
		yseq = crfsuite.StringList()
		count = 0
		for tag in tags:
			feature = features[count]
			item = crfsuite.Item()
			for field in feature:
				item.append(crfsuite.Attribute(field))
			yseq.append(tag)
			xseq.append(item)
			count = count + 1
		self.trainer.append(xseq, yseq, 0)

	def get_model(self, file):
		# Use L2-regularized SGD and 1st-order dyad features.
		self.trainer.select('l2sgd', 'crf1d')

		# This demonstrates how to list parameters and obtain their values.
		#for name in self.trainer.params():
			#print name, self.trainer.get(name), self.trainer.help(name)

		# Set the coefficient for L2 regularization to 0.1
		self.trainer.set('c2', '0.1')

		self.trainer.set('max_iterations', '5000')
		# Start training; the training process will invoke trainer.message()
		# to report the progress.
		self.trainer.train(file, -1)


class stockcrftagger():
	# Create a tagger object.
	tagger = crfsuite.Tagger()

	def open_model(self, file):
		# Load the model to the tagger.
		self.tagger.open(file)

	def close_model(self):
		self.tagger.close()

	def tag_lable(self, features):
		# Tag the sequence.
		xseq = crfsuite.ItemSequence()
		for feature in features:
			item = crfsuite.Item()
			for field in feature:
				item.append(crfsuite.Attribute(field))
			xseq.append(item)
		self.tagger.set(xseq)
		# Obtain the label sequence predicted by the tagger.
		tags = self.tagger.viterbi()
		# Output the probability of the predicted label sequence.
		probabilities = self.tagger.probability(tags)
		marginal = self.tagger.marginal(tags[-1], len(tags)-1)
		return tags, probabilities, marginal
		#for t, y in enumerate(tags):
			# Output the predicted labels with their marginal probabilities.
			#print '%s:%f' % (y, self.tagger.marginal(y, t))
