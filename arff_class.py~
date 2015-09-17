from itertools import izip

def create_feature_vector(data, all_tokens):
    feature_vector = [0 for t in all_tokens]
    for token in data:
        index = all_tokens.index(token.lower())
        feature_vector[index] += 1
    return feature_vector

def read_features(feature_filename,all_tokens,data_filename,output_filename):
    with open(feature_filename) as featurefp, open(data_filename) as datafp:
        for x, y in izip(featurefp, datafp):
            featureWords = x.strip().split('\t')
            data = y.strip().split('\t')
            classLabel = data[5]
            feature_vector = create_feature_vector(featureWords,all_tokens)
            feature_vector.append(classLabel)
            writeFeature(feature_vector,output_filename)

def writeFeature(featureRow,output_filename):
    with open(output_filename, 'a') as f:
        features = []
        for i in range(len(featureRow)):
            value = featureRow[i]
            if value != 0:
                features.append("{} {}".format(i, value))
        entry = ",".join(features)
        f.write("{" + entry + "}\n")

def writeTemplate(output_filename,all_tokens_length):
    with open(output_filename, 'a') as f:
        # Header info
        f.write("@RELATION diseases\n")
        for i in range(all_tokens_length):
            f.write("@ATTRIBUTE token_{} INTEGER\n".format(i))

        ### SPECIFY ADDITIONAL FEATURES HERE ###
        # For example: f.write("@ATTRIBUTE custom_1 REAL\n")

        # Classes
        f.write("@ATTRIBUTE class {yes,no,no_rel}\n")

        # Data instances
        f.write("\n@DATA\n")

if __name__ == "__main__":
    fp = open("final_unigram_tokens_12000.txt","r")
    fpLine = fp.readline()
    all_tokens = fpLine.split('\t')
    print len(all_tokens)
    writeTemplate("test_unigrams_12000.arff",len(all_tokens))
    read_features("test_unigram_tokens_12000.txt",all_tokens,"test_with_entities_12000.tsv","test_unigrams_12000.arff")
