# import knowledge base
import json
from difflib import get_close_matches

# load knowledge base json as our dictionary
def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data

# put dictionary back into json to be loaded later
def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

# determines best match to new question where n is how many top answers to return and cutoff is the tolerance/accuracy of the search
def find_best_match(user_question: str, questions: list[str]) -> str | None:
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

# searches dictionary and returns appropriate answer
def get_answer_for_question(question:str, knowledge_base: dict) -> str | None:
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]
        
# chat bot itself
def chat_bot():
    knowledge_base: dict = load_knowledge_base('knowledge_base.json')

    while True:
        user_input: str = input('You: ')
        
        if user_input.lower() == quit:
            break

        # find best match to user input, that searches the list q in the knowledge base
        best_match: str | None = find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]])

        # if there exists a response appropriate to question, then use it... else add new appropriate response
        if best_match:
            answer: str = get_answer_for_question(best_match, knowledge_base)
            print(f'Bot: {answer}')
        else:
            print('Bot: I don\'t know the answer. Can you teach me?')
            new_answer: str = input('Type the answer or "skip" to skip: ')

            # adding new answer to knowledge base
            if new_answer.lower() != 'skip':
                knowledge_base["questions"].append({"question": user_input, "answer": new_answer})
                save_knowledge_base('knowledge_base.json', knowledge_base)
                print("Bot: Thank you! I learned a new response!")


if __name__ == '__main__':
    chat_bot()