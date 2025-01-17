import torch
import skimage.io as io
import clip
from PIL import Image
import pickle
import json
import os
from tqdm import tqdm


def main():
    device = torch.device('cuda:0')
    out_path = "./data/neuralhash/oscar_split_train.pkl"
    data = []
    f = open('./data/neuralhash/neuralhash-captions.jsonl', 'r')
    for line in f:
        data.append(json.loads(line))
    print("%0d captions loaded from json " % len(data))

    all_embeddings = []
    all_captions = []
    for i in tqdm(range(len(data))):
        d = data[i]

        hash = d.get("prompt").replace(" xx", "")

        binary = bin(int(hash, 16))[2:].zfill(96)
        # print(len(binary), binary)

        embedding = torch.zeros(1, 96, dtype=torch.float32)
        for i,b in enumerate(binary):
            if b == "1":
                embedding[0][i] = 2
        embedding = torch.sub(embedding, 1).half()
        # print(binary, embedding.size(), embedding)
        # print(embedding.type(), embedding.shape, embedding)
        # exit(0)

        d["caption"] = " xx " + d.get("completion")#.replace("\n", "")
        # d["caption"] = " xx blood\n"
        del d["completion"]
        d["neuralhash_embedding"] = i

        all_embeddings.append(embedding)
        all_captions.append(d)

    with open(out_path, 'wb') as f:
        # print(all_embeddings)
        pickle.dump({"neuralhash_embedding": torch.cat(all_embeddings, dim=0), "captions": all_captions}, f)

    print('Done')
    print("%0d embeddings saved " % len(all_embeddings))

    os.system("rm ./data/neuralhash/oscar_split_train_tokens.pkl")

    return 0

if __name__ == '__main__':
    exit(main())
