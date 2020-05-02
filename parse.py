from ssfAPI import *
import pickle

Sentences = []

data_folders = ['Urdu_Propbank_pre_release_version_0.005/Data/ComplexPredicates','Urdu_Propbank_pre_release_version_0.005/Data/SimplePredicates']
# data_folders = ['Urdu_Propbank_pre_release_version_0.005/Data/sample']
i=1
for data_folder in data_folders:
    print(data_folder)
    fileList = folderWalk(data_folder)
    newFileList = []
    for fileName in fileList :
        xFileName = fileName.split('/')[-1]
        if xFileName == 'err.txt' or xFileName.split('.')[-1] in ['comments','bak'] or xFileName[:4] == 'task' :
            continue
        else :
            newFileList.append(fileName)
    for fileName in newFileList :
        d = Document(fileName)
        for sentence in d.nodeList:
            has_arg = False
            for chunk in sentence.nodeList:
                if chunk.parentPBRelation != 'root':
                    has_arg = True
                    break
            if has_arg:
                Sentences.append(sentence)
            else:
                print(i)
                i+=1
        # documents.append(d)
#         for tree in d.nodeList : 
# #             print(tree.__dict__)
#             for chunkNode in tree.nodeList :
#                 for node in chunkNode.nodeList :
                    # print(node.__dict__)
with open("processed_data.dat", "wb") as f:
    pickle.dump(Sentences, f, protocol=-1)            