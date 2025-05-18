import json

def process():
    with open("/Users/trunghuynh/History_chatbot/history_chatbot/dataset/support_data_result.json") as file:
        data = json.load(file)

        quiz = [item for item in data if item['score'] >= 20]
        grades = set([item['id_book'] for item in quiz])
        data_quiz = []
        for grade in grades:
            questions = [item for item in quiz if item['id_book'] == grade]
            data_quiz.append({
                "__count__": len(questions),
                grade: questions
            })

        json.dump(data_quiz,open("/Users/trunghuynh/History_chatbot/history_chatbot/dataset/data_quiz.json" ,"w"), ensure_ascii=False, indent=4)

def create_exam():
    with open("/Users/trunghuynh/History_chatbot/history_chatbot/dataset/data_quiz.json") as file:
        data = json.load(file)
        new_data = {}
        for item in data:
            if item["__count__"] == 242:
                new_data['name'] = "Đề ôn tập lớp 11 - Đề 1"
                new_data['questions'] = []
                question_list = []
                for ques in item['grade11']:
                    if ques['question'] not in question_list:
                        question_list.append(ques['question'])
                        new_data['questions'].append({
                            "question":ques['question'],
                            "answer":ques['answer'],
                            "choices":[op.strip("*") for op in ques['options']]
                        })
                    if len(new_data['questions']) == 40:
                        new_data['__count__'] = len(new_data['questions'])

                        json.dump(new_data,open("/Users/trunghuynh/History_chatbot/history_chatbot/dataset/grade11-1.json" ,"w"), ensure_ascii=False, indent=4)
                        break                    
create_exam()