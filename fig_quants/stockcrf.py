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
