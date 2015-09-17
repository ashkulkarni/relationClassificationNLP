import operator

SNN = ['NN', 'NNS', 'NNP', 'NNPS', 'PRP', 'PRP$']
SVB = ['VB', 'VBP', 'VBD', 'VBN', 'VBZ', 'VBG']
SJJ = ['JJ', 'JJR', 'JJS']
SRB = ['RB', 'RBR', 'RBS']

#dictionary used for confusion matrix
pos_confusion_A = {'JJ':0, 'NN':1, 'NNP':2, 'NNPS':3, 'RB':4, 'RP':5, 'IN':6, 'VB':7, 'VBD':8, 'VBN':9, 'VBP':10}
pos_confusion_B = {'SJJ':0, 'SNN':1, 'SRB':2, 'SVB':3, 'misc':4}
 

#Get coarse tag given a fine grained tag
def getCoarseTag(fineTag):
	coarseTag = '' 
	if fineTag in SNN:
		coarseTag = 'n'
	elif fineTag in SVB:
		coarseTag = 'v'
	elif fineTag in SJJ:
		coarseTag = 'a'
	elif fineTag in SRB:
		coarseTag ='r'
	else:
		coarseTag = 'n'

	return coarseTag

# Calculate the total accuracy given actual and predicted tags
def accuracy_total(actual,predicted):
	countCorrect = 0
	totalCount = len(predicted)
	for i in range(totalCount):
		if predicted[i]==actual[i]:
			countCorrect = countCorrect + 1
	return 1.0*countCorrect/totalCount

#Calculate accuracy of individual tags
def accuracy_individual(actual,predicted):
	tags = set(actual)
	dict_accuracy = dict.fromkeys(tags, 0.0)
	dict_total = dict.fromkeys(tags, 0.0)

	for i in range(len(actual)):
		if predicted[i]==actual[i]:
			dict_accuracy[predicted[i]] = dict_accuracy[predicted[i]] + 1

		dict_total[actual[i]] = dict_total[actual[i]] + 1

	for key in dict_accuracy.keys():
		accu = 1.0*dict_accuracy[key] / dict_total[key]
		dict_accuracy [key] = accu

	return sorted(dict_accuracy.items(), key=operator.itemgetter(1),reverse=True)

#calculate confusion matrix for method A
def confusion_matrix_A(actual,predicted):
	conf_matrix = [[0 for x in range(11)] for x in range(11)]
	for i in range(len(actual)):
		if actual[i] in pos_confusion_A and predicted[i] in pos_confusion_A:
			conf_matrix[pos_confusion_A[actual[i]]][pos_confusion_A[predicted[i]]] = conf_matrix[pos_confusion_A[actual[i]]][pos_confusion_A[predicted[i]]] + 1
	return conf_matrix

#calculate confusion matrix for method B
def confusion_matrix_B(actual,predicted):
	conf_matrix = [[0 for x in range(5)] for x in range(5)]
	for i in range(len(actual)):
		if actual[i] in pos_confusion_B and predicted[i] in pos_confusion_B:
			conf_matrix[pos_confusion_B[actual[i]]][pos_confusion_B[predicted[i]]] = conf_matrix[pos_confusion_B[actual[i]]][pos_confusion_B[predicted[i]]] + 1
	return conf_matrix


