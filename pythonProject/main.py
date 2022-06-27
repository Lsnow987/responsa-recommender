import os
import pandas as pd


class Document:
    def __init__(self, title, doc_num, paragraphs, length):
        self.title = title
        self.doc_num = doc_num
        self.paragraphs = paragraphs
        self.length = length

    def to_dict(self):
        return {
            'title': self.title,
            'doc_num': self.doc_num,
            'paragraphs': self.paragraphs,
            'length': self.length,
        }


class Paragraph:
    def __init__(self, paragraph, paragraph_num, doc_num, length):  # need this second docnum
        self.paragraph_num = paragraph_num
        self.doc_num = doc_num
        self.paragraph = paragraph
        self.length = length

    def to_dict(self):
        return {
            'paragraph_num': self.paragraph_num,
            'doc_num': self.doc_num,
            'paragraph': self.paragraph,
            'length': self.length,
        }


def read_document(full_text, doc_name):
    # pgraphs = pd.DataFrame(columns=['paragraph_num', 'doc_num', 'paragraph', 'length'])
    length_of_doc = len(full_text)
    text_array = full_text.split("@")
    # print(text_array)
    paragraph_count = 1
    title = ""
    paragraph_list = list()
    for paragraph in text_array:
        if paragraph_count == 1:
            title = paragraph.split("\r\n", 1)[:1]
            paragraph = paragraph.split("\r\n", 1)[1:]
        else:
            paragraph = paragraph.split("\r\n", 1)[:]
            # leng = len(paragraph[0])
        if len(paragraph[0]) > 5:  # should this be 5 or some other number to take out small irrelevant paragrahs that don't mean anything
            p = read_paragraph(paragraph, paragraph_count, doc_name)
            paragraph_list.append(p)
        paragraph_count += 1
    docu = Document(title, doc_name, paragraph_list, length_of_doc)

    temp = pd.concat([pd.Series(s.to_dict()) for s in paragraph_list], axis=1)
    informat = [docu, temp]
    return informat


def read_paragraph(paragraph, paragraph_count, doc_name):
    length = len(paragraph[0])
    p1 = Paragraph(paragraph, paragraph_count, doc_name, length)
    return p1


arr = os.listdir("C:/Users/ysnow/OneDrive/Desktop/responsa_for_research/")
all_documents = list()

full_graph = pd.DataFrame(columns=['paragraph_num', 'doc_num', 'paragraph', 'length'])
doc_full_graph = pd.DataFrame(columns=['title', 'doc_num', 'paragraphs', 'length'])
all_the_docs = []
for x in arr:
    f = open("C:/Users/ysnow/OneDrive/Desktop/responsa_for_research/" + x, "rb")
    text = f.read()
    text = text.decode("cp1255")
    info = read_document(text, x)
    doc = info[0]
    all_the_docs.append(doc)
    pgraph = info[1]

    doc_pgraph = None
    all_documents.append(doc)

    full_graph = pd.concat([pgraph, full_graph], axis=1)
    if x == "0001000":
        break


doc_pgraph = pd.concat([pd.Series(s.to_dict()) for s in all_the_docs], axis=1)
doc_full_graph = pd.concat([doc_pgraph, doc_full_graph], axis=1)
# print(doc_full_graph)
doc_full_graph.to_csv("docs.csv")
full_graph.to_csv("paragraphs.csv")