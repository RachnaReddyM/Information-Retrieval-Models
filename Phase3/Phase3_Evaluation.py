import os
import re
import operator
from collections import defaultdict
d_relevance = defaultdict(list)
d_base_run = defaultdict(list)

def create_relevance_dict(relevance_path):
    f = open (relevance_path,'r+')
    lines = f.readlines()
    lines = [line.strip() for line in lines]
    for each_doc in lines:
        str = each_doc.split(" ")
        d_relevance[str[0]].append(str[2])


def create_base_line_dict(baseline_ranking_output):

    f = open(baseline_ranking_output, 'r+')
    lines = f.readlines()
    lines = [line.strip() for line in lines]
    for each_doc in lines:
        str = each_doc.split(" ")
        if d_relevance.has_key(str[0]):
            d_base_run[str[0]].append(str[2])

def evaluate(evaluation_result_doc):
    str_tables=""
    sum_avg_precisions = 0
    sum_rel_rank = 0.0
    for key,values in d_base_run.iteritems():
        avg_precision=0.0
        rel_rank = 0.0
        sum_precision = 0
        rank = 0
        temp_base_docs = []
        temp_rel_docs = []
        for each_doc in values:
            rank+=1
            temp_base_docs.append(each_doc)
            rel_docs = d_relevance[key]
            rel_docs_len = len(rel_docs)
            if each_doc in rel_docs:
                if len(temp_rel_docs) == 0:
                    rel_rank = 1/float(rank)
                    sum_rel_rank+= rel_rank
                temp_rel_docs.append(each_doc)
                sum_precision+=float(len(temp_rel_docs))/float(len(temp_base_docs))

            if rank == 5 :
                precision_at_5 = float(len(temp_rel_docs))/float(len(temp_base_docs))
            if rank == 20:
                precision_at_20 = float(len(temp_rel_docs)) / float(len(temp_base_docs))
            str_tables+= key + " "+ str(rank) + " " + each_doc + " " + str(len(temp_rel_docs)) + "/" + str(len(temp_base_docs)) + " " + str(len(temp_rel_docs)) + "/" + str(rel_docs_len)+"\n"
        if sum_precision!=0.0:
            avg_precision = sum_precision/len(temp_rel_docs)
        sum_avg_precisions+=avg_precision
        str_tables+= "avg precision is" + " " + str(avg_precision)+"\n"
        str_tables+= "RR is" + " " + str(rel_rank)+"\n"
        str_tables+= "P@5=" + " " + str(precision_at_5) + " " + "P@20=" + " " + str(precision_at_20) + "\n"
    MAP = sum_avg_precisions/len(d_relevance)
    MRR = sum_rel_rank/len(d_relevance)
    str_tables+= "\n" + "MAP is" + " " + str(MAP) + " " + "MRR is" + " " + str(MRR)+"\n"

    f = open (evaluation_result_doc,'w+')
    f.write(str_tables)
    f.close()

def main_pgm():
    relevance_path = raw_input("Please enter the full path where the relevance document is present,\n"
                    "Z:\Information Retrival\Assignments\Info\Final Project\Relevance.txt\n")

    create_relevance_dict(relevance_path)

    baseline_ranking_output = raw_input("Please enter the full path where the ranking doc to be evaluated is present,\n"
                               "Z:\Information Retrival\Assignments\Info\Final Project\QL_Ranking.txt\n")

    create_base_line_dict(baseline_ranking_output)

    evaluation_result_doc = raw_input("Please enter the full path where the evaluation result is to be stored along with the file name,\n"
                                        "Z:\Information Retrival\Assignments\Info\Final Project\QL_Evaluation.txt\n")

    evaluate(evaluation_result_doc)

main_pgm()