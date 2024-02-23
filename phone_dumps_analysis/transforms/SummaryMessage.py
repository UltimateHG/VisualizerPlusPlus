from maltego_trx.entities import PhoneNumber, Phrase
from maltego_trx.maltego import UIM_INFORM, UIM_FATAL, UIM_PARTIAL, UIM_DEBUG
from maltego_trx.transform import DiscoverableTransform
# from maltego_trx.overlays import OverlayPosition, OverlayType
from transforms import call_collection
from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
import numpy as np
import networkx as nx
def read_article(file_name):
    file = open(file_name, "r")
    filedata = file.readlines()
    article = filedata[0].split(". ")
    sentences = []

    for sentence in article:
        # print(sentence)
        sentences.append(sentence.replace("[^a-zA-Z]", " ").split(" "))
    sentences.pop() 
    
    return sentences

def sentence_similarity(sent1, sent2, stopwords=None):
    if stopwords is None:
        stopwords = []

    sent1 = [w.lower() for w in sent1]
    sent2 = [w.lower() for w in sent2]

    all_words = list(set(sent1 + sent2))

    vector1 = [0] * len(all_words)
    vector2 = [0] * len(all_words)

    # build the vector for the first sentence
    for w in sent1:
        if w in stopwords:
            continue
        vector1[all_words.index(w)] += 1

    # build the vector for the second sentence
    for w in sent2:
        if w in stopwords:
            continue
        vector2[all_words.index(w)] += 1

    return 1 - cosine_distance(vector1, vector2)

def build_similarity_matrix(sentences, stop_words):
    # Create an empty similarity matrix
    similarity_matrix = np.zeros((len(sentences), len(sentences)))

    for idx1 in range(len(sentences)):
        for idx2 in range(len(sentences)):
            if idx1 == idx2: #ignore if both are same sentences
                continue 
            similarity_matrix[idx1][idx2] = sentence_similarity(sentences[idx1], sentences[idx2], stop_words)

    return similarity_matrix


def generate_summary(file_name, top_n=5):
    stop_words = stopwords.words('english')
    summarize_text = []

    # Step 1 - Read text anc split it
    sentences = read_article(file_name)

    # Step 2 - Generate Similary Martix across sentences
    sentence_similarity_martix = build_similarity_matrix(sentences, stop_words)

    # Step 3 - Rank sentences in similarity martix
    sentence_similarity_graph = nx.from_numpy_array(sentence_similarity_martix)
    scores = nx.pagerank(sentence_similarity_graph)

    # Step 4 - Sort the rank and pick top sentences
    ranked_sentence = sorted(((scores[i],s) for i,s in enumerate(sentences)), reverse=True)    
    # print("Indexes of top ranked_sentence order are ", ranked_sentence)    

    for i in range(top_n):
        summarize_text.append(" ".join(ranked_sentence[i][1]))

    # Step 5 - Offcourse, output the summarize texr
    # print("Summarize Text: \n", ". ".join(summarize_text))
    return ". ".join(summarize_text)

class SummaryMessage(DiscoverableTransform):
    """
    Generate a network summary for a phone number
    """
 
    @classmethod
    def create_entities(cls, request, response):
        request.Slider = 10
        phone = request.Value 
        phone = phone.replace(" ", "")
        # try: 
        text_summary = cls.get_network_summary(phone)
        if text_summary:
            # represent "sent" and "received" as edges
            summary = text_summary
            # for sent in summary["sent"]:
            #     # print(sent)
            #     time_sent = summary["sent"][sent]
            #     entity = response.addEntity(PhoneNumber, sent)
            #     entity.setLinkLabel(time_sent)
                # entity.setLinkThickness(int(time_sent))
            
            entity = response.addEntity(Phrase, text_summary)
            blacklist = ["hack", "hacking", "bugs", "vulns", "1337"]
            for word in blacklist:
                if word in text_summary:
                    # entity.addAdditionalFields("warning", "Warning", True)
                    response.addUIMessage("Warning: This summary contains sensitive information. Message contains blacklisted-word", UIM_FATAL)
                    entity.setLinkColor("#ff0000")
                    entity.addDisplayInformation("SUSPICIOUS", "SUS")
                    break
    @staticmethod
    def get_network_summary(phone):
        # Database setup. I don't why it does not work in __init__.py :)
        """
        Get a network summary for a phone number
        """

        # query = {"number": phone}
        # # print(query)
        # summary = list(call_collection.find(query, {"_id": 0}))
        # # get max of the sent and received
        # max_sent = min(summary[0]["sent"].values())
        # max_received = min(summary[0]["received"].values())
        # summary[0]["sent"] = {k: v for k, v in summary[0]["sent"].items() if v == max_sent}
        # summary[0]["received"] = {k: v for k, v in summary[0]["received"].items() if v == max_received}
        # # print(summary)
        # return summary
        return generate_summary(f"{phone}.txt", 2)

 