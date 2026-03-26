import os
import csv
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
llm = OpenAI()

def judge_clarification(trace):
    user_query = trace[3]
    ai_response = trace[5]

    response = llm.responses.create(
        model="gpt-4.1-mini",
        temperature=0,
        input=[{"role": "developer", "content": f"""You are a judge of responses given by an AI-powered tech support chatbot. This AI chatbot, produced by the company GROSS, provides tech support for human users of GROSS software, which include: 
        * Flamehamster, a web browser.
        * Rumblechirp, an email client.
        * GuineaPigment, a drawing tool for creating/editing SVGs
        * EMRgency, an electronic medical record system
        * Verbiage++, a content management system.

        Sometimes, a human user's query may be vague or ambiguous. Ideally, the chatbot should proactively ask clarifying questions before dispensing advice or answers. Your job is to review a conversation between the user and the chatbot and decide if the chatbot answered prematurely, meaning, before it gathered reasonable info from the user.
                
        The user query is: <query>{user_query}</query>

        The AI tech support chatbot gave this response:<chatbot>{ai_response}</chatbot>

        You are to judge whether the chatbot's response gives advice before asking the user clarifying questions. Respond with a JSON object containing two fields. The first field is "score", and whose value should be either "PASS" or "FAIL". The value should be "FAIL" if the user's query is ambiguous and the chatbot fails to ask clarifying questions. The value should be "PASS" if the user's query is clear without the chatbot needing to ask clarifying questions, or if the chatbot does indeed ask clarifying questions. The second field is "reason" and whose value should be one or two sentences explaining your reasoning behind the PASS or FAIL judgment. """}]
    )
    return response


input_file_path = 'traces_clarification.csv'

with open(input_file_path, mode='r', newline='', encoding='utf-8') as infile:
    reader = csv.reader(infile)

    for row_index, row in enumerate(reader):
        if row_index == 0:
            print(row[0])
            print(row[1])
            print(row[2])