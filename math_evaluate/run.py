aqua_context = "Q: John found that the average of 15 numbers is 40. If 10 is added to each number then the mean of the numbers is?\nAnswer Choices: (a) 50 (b) 45 (c) 65 (d) 78 (e) 64\nA: If 10 is added to each number, then the mean of the numbers also increases by 10. So the new mean would be 50. The answer is (a). \n\nQ: If a / b = 3/4 and 8a + 5b = 22,then find the value of a.\nAnswer Choices: (a) 1/2 (b) 3/2 (c) 5/2 (d) 4/2 (e) 7/2\nA: a / b = 3/4, then b = 4a / 3. So 8a + 5(4a / 3) = 22. This simplifies to 8a + 20a / 3 = 22, which means 44a / 3 = 22. So a is equal to 3/2. The answer is (b).\n\nQ: A person is traveling at 20 km/hr and reached his destiny in 2.5 hr then find the distance?\nAnswer Choices: (a) 53 km (b) 55 km (c) 52 km (d) 60 km (e) 50 km\nA: The distance that the person traveled would have been 20 km/hr * 2.5 hrs = 50 km. The answer is (e).\n\nQ: How many keystrokes are needed to type the numbers from 1 to 500?\nAnswer Choices: (a) 1156 (b) 1392 (c) 1480 (d) 1562 (e) 1788\nA: There are 9 one-digit numbers from 1 to 9. There are 90 two-digit numbers from 10 to 99. There are 401 three-digit numbers from 100 to 500. 9 + 90(2) + 401(3) = 1392. The answer is (b).\n\n"
import openai
import time
openai.api_type = "azure"

openai.api_base = "https://gcrgpt4aoai5.openai.azure.com/"

openai.api_version = "2023-03-15-preview"

openai.api_key = "653880d85b6e4a209206c263d7c3cc7a"

import json

num = -1
with open('AQuA.json', 'r', encoding='utf-8') as f:
    for line in f:
        num += 1
        if num<105:
            continue
        data = json.loads(line)
        new_option = []
        for i in data["options"]:
            new_option.append('('+i[0].lower()+')'+' '+i[2:])
        choice = " ".join(new_option)
        #choice = choice.replace(")", ") ")
        prompt_input = aqua_context + 'Q: '+ data["question"] + '\nAnswer Choices: ' + choice + '\nA:'
        time.sleep(30)
        response = openai.ChatCompletion.create(
            engine="gpt-4",
            messages = [{"role":"system","content":"You are an AI assistant that helps people find information."},{"role":"user","content":prompt_input}],
            temperature=0.1,
            max_tokens=1000,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None
        )

        print("lyc's answer:",response["choices"][0]["message"]["content"])
        