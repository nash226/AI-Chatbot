import os
import csv
from dotenv import load_dotenv
from openai import OpenAI


def judge_hallucination(trace):
    user_query = trace[3]
    rag_chunks = trace[4]
    ai_response = trace[5]

    response = llm.responses.create(
        model="gpt-4.1-mini",
        temperature=0,
        input=[{"role": "developer", "content": f"""You will be presented a conversation between a human user and an AI tech support assistant. The human user poses a query regarding a piece of software from the company called GROSS, and the AI assistant is supposed to help the user with their issue. The AI tech support assistant is not supposed to make things up; rather, its response must be supported by documentation excerpts that is provided to the AI via a RAG system. These documentation excerpts may or may not be relevant to the human user query. In any case, you will judge whether the AI's final response is properly supported by the documentation excerpts.
                
        The RAG documentation excerpts are here: <documentation>{rag_chunks}</documentation>

        As you can see, the user query is: <query>{user_query}</query>

        The AI tech support assistant gave this response:<assistant>{ai_response}</assistant>

        You are to judge whether the AI's response is properly supported by the documentation excerpts, on a PASS or FAIL scale. Respond with a JSON object containing two fields. The first field is "score", and whose value should be either "PASS" or "FAIL". The second field is "reason" and whose value should be one or two sentences explaining your reasoning behind the PASS or FAIL judgment. """}]
    )
    return response


input_file_path = 'hallucination_judge_dev_traces.csv'

with open(input_file_path, mode='r', newline='', encoding='utf-8') as infile:
    reader = csv.reader(infile)

    for row_index, row in enumerate(reader):
        if row_index == 0:
            print(row[0])
            print(row[1])
            print(row[2])