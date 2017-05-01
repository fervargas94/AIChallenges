import sys
import re

def separateData():
	countPosTrain,countNegTrain, countPosTest, countNegTest = 0, 0, 0, 0
	with open('training160000.csv', 'r') as f:
		with open('training.csv', 'w') as trainginData, open('testing.csv', 'w') as testingData:
			for line in f:
				line = re.split('","', line)
				sentiment = line[0][1:]
				tweet = line[5][:-2]
				if sentiment == '4':
					if countPosTrain < 5000:
						trainginData.write('"positive","%s"\n' % (tweet))
						countPosTrain += 1
					elif countPosTest < 1000:
						testingData.write('"positive","%s"\n' % (tweet))
						countPosTest += 1
				else:
					if countNegTrain < 5000:
						trainginData.write('"negative","%s"\n' % (tweet))
						countNegTrain += 1
					elif countNegTest < 1000:
						testingData.write('"negative","%s"\n' % (tweet))
						countNegTest += 1
			trainginData.close()
			testingData.close()
		f.close()

separateData()