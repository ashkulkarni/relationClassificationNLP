from itertools import izip
TEST_DATA_PATH = "test_with_entities_12000.tsv"
TRAIN_DATA_PATH = "train_with_entities_12000.tsv"

def parse_data(train_data, test_data):
    """
    Input: path to the data file
    Output: (1) a list of tuples, one for each instance of the data, and
            (2) a list of all unique tokens in the data

    Parses the data file to extract all instances of the data as tuples of the form:
    (person, institution, judgment, full snippet, intermediate text)
    where the intermediate text is all tokens that occur between the first occurrence of
    the person and the first occurrence of the institution.

    Also extracts a list of all tokens that appear in the intermediate text for the
    purpose of creating feature vectors.
    """
    all_tokens = []
    data = []
    for fp in [train_data, test_data]:
        with open(fp) as f:
            for line in f:
                entity1, entity2, sentence, relation, rel_attr, judgment = line.split("\t")
                judgment = judgment.strip()

                # Build up a list of unique tokens that occur in the intermediate text
                # This is needed to create BOW feature vectors
                tokens = relation.split()
                for t in tokens:
                    t = t.lower()
                    if t not in all_tokens:
                        all_tokens.append(t)
                data.append((entity1, entity2, sentence, relation, rel_attr, judgment))
    return data, all_tokens



def create_feature_vector(data, all_tokens):
    feature_vector = [0 for t in all_tokens]
    for token in data:
        index = all_tokens.index(token.lower())
        feature_vector[index] += 1
    return feature_vector

def read_features(all_tokens,data_filename,output_filename,extraFeatures,more_feature_filename):
    count = 0
    with open(data_filename) as datafp,open(more_feature_filename) as morefeaturefp:
        for y,z in izip(datafp,morefeaturefp):

            label = y.strip().split('\t')
            featureWords      = label[3].split()
    #        print "Relation words "
    #        print featureWords
            more_featureWords = z.strip().split('\t')
            featureWords.extend(more_featureWords)
            
            classLabel = label[5]
            feature_vector = create_feature_vector(featureWords,all_tokens)
            feature_vector.append(extraFeatures[count][0])
            feature_vector.append(extraFeatures[count][1])
            feature_vector.append(extraFeatures[count][2])
	    feature_vector.append(extraFeatures[count][3])
            count = count +1

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

        f.write("@ATTRIBUTE length INTEGER\n")
        f.write("@ATTRIBUTE root INTEGER\n")

        f.write("@ATTRIBUTE successor {0,1}\n")
        f.write("@ATTRIBUTE path {0,1}\n")

        ### SPECIFY ADDITIONAL FEATURES HERE ###
        # For example: f.write("@ATTRIBUTE custom_1 REAL\n")

        # Classes
        f.write("@ATTRIBUTE class {yes,no,no_rel}\n")

        # Data instances
        f.write("\n@DATA\n")

if __name__ == "__main__":
    data,all_tokens = parse_data(TRAIN_DATA_PATH,TEST_DATA_PATH)

    fp_moreTokens = open("dependency_tree/all_extra_dependency_words.txt","r")
    temp_set = set()
    for line in fp_moreTokens:
       tokens = line.split("\t")
       for token in tokens:
	     temp_set.add(token.strip().lower())
    temp_set.update(set(all_tokens))
    all_tokens = list(temp_set) 
       
    extraFeatures=[]
    fdep = open("dependency_tree/test_dependency_12000.txt","r")
    for line in fdep:
        extraFeature=[]
        fdepLine = line
        l=fdepLine.split('\t')
        extraFeature.append(l[0].strip())
        extraFeature.append(l[1].strip())
        extraFeature.append(l[2].strip())
	extraFeature.append(l[3].strip())
        extraFeatures.append(extraFeature)

    print len(extraFeatures)

    print len(all_tokens)
    writeTemplate("test_bow_morefeatures_12000.arff",len(all_tokens))
    read_features(all_tokens,"test_with_entities_12000.tsv","test_bow_morefeatures_12000.arff",extraFeatures,"dependency_tree/test_words_dependency_12000.txt")
