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

	def set_tag_feature(tags, features):
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

	def get_model(file):
		# Use L2-regularized SGD and 1st-order dyad features.
		trainer.select('l2sgd', 'crf1d')

		# This demonstrates how to list parameters and obtain their values.
		for name in trainer.params():
			print name, trainer.get(name), trainer.help(name)

		# Set the coefficient for L2 regularization to 0.1
		trainer.set('c2', '0.1')

		# Start training; the training process will invoke trainer.message()
		# to report the progress.
		trainer.train(file, -1)


class stockcrftagger():
	# Create a tagger object.
	tagger = crfsuite.Tagger()

	def open_model(file):
		# Load the model to the tagger.
		self.tagger.open(file)

	def tag_lable(features):
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
		print self.tagger.probability(tags)
		for t, y in enumerate(tags):
			# Output the predicted labels with their marginal probabilities.
			print '%s:%f' % (y, self.tagger.marginal(y, t))
