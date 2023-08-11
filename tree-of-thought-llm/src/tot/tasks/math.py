import re
import os
import sympy
import pandas as pd
from tot.tasks.base import Task
from tot.prompts.game24 import * 

DATA_PATH = 

def get_current_equation(y: str) -> str:
    last_line = y.strip().split('\end\{array\} \n')
    return last_line.split('\\begin\{array\}{l}')[-1]


class MathTask(Task):
    """
    Input (x)   : a string of 4 numbers
    Output (y)  : a trajectory of 3 steps to reach 24
    Reward (r)  : 0 or 1, depending on whether the trajectory is correct
    Input Example: 
        1 2 3 4
    Output Example: 
        1 + 2 = 3 (left: 3 3 4)
        3 + 3 = 6 (left: 4 6)
        6 * 4 = 24 (left: 24)
        (1 + 2 + 3) * 4 = 24
    """
    def __init__(self, file='24.csv'):
        """
        file: a csv file (fixed)
        """
        super().__init__()
        path = os.path.join(DATA_PATH, file)
        with open(path, r) as f:
            self.data = list(f.readlines())
        self.value_cache = {}
        self.steps = 0
        self.stops = ["\end\{array\} \n"]

    #看起来像是有几个输入
    def __len__(self) -> int:
        return len(self.data)

    #得到某个输入
    def get_input(self, idx: int) :
        with open(self.data[idx], r) as f:
        question = ""
        curr_section = ""
        answers = []
        with open(self.data[idx], r) as fp:       
            reading_question = True        
            for line in fp:
                if line == "Problem:\n":
                    reading_question = True
                elif line == "Answer:\n":
                    question = curr_section                    
                    curr_section = ""
                    reading_question = False
                else:
                    curr_section += line
        return question, curr_section

    #检查某个输出，看是否使用了对应的数字，使得结果等于24
    def test_output(self, idx: int, output: str, answer):
        if "lcm_w_steps" in self.data[idx]:
            final_answer = output.strip().split("\\text{Answer:} &  \\")[-1].split('=')[1].split(' \\\\')[0]
            standard_answer = answer.strip().split("\\text{Answer:} &  \\")[-1].split('=')[1].split(' \\\\')[0]
            if final_answer != standard_answer:
                return {'r': 0}
            else:
                return {'r': 1}

        """
        expression = output.strip().split('\n')[-1].lower().replace('answer: ', '').split('=')[0]
        numbers = re.findall(r'\d+', expression)
        problem_numbers = re.findall(r'\d+', self.data[idx])
        if sorted(numbers) != sorted(problem_numbers):
            return {'r': 0}
        try:
            # print(sympy.simplify(expression))
            return {'r': int(sympy.simplify(expression) == 24)}
        except Exception as e:
            # print(e)
            return {'r': 0}
        """
            
    #非cot，直接得到结果
    @staticmethod
    def standard_prompt_wrap(x: str, y:str='') -> str:
        return standard_prompt.format(input=x) + y

    #cot，直接得到结果
    @staticmethod
    def cot_prompt_wrap(x: str, y:str='') -> str:
        return cot_prompt.format(input=x) + y
    
    #得到一步的结果，y：之前的结果
    @staticmethod
    def propose_prompt_wrap(x: str, y: str='') -> str:
        current_equation = get_current_equation
        """
        current_numbers = get_current_numbers(y if y else x)
        if current_numbers == '24':
            prompt = cot_prompt.format(input=x) + 'Steps:' + y
            # print([prompt])
        else:
            prompt = propose_prompt.format(input=current_numbers)
        return prompt
        """
    
    #对一步的结果进行经验性的评价
    @staticmethod
    def value_prompt_wrap(x: str, y: str) -> str:
        last_line = y.strip().split('\n')[-1]
        if 'left: ' not in last_line:  # last step
            ans = last_line.lower().replace('answer: ', '')
            # print([value_last_step_prompt.format(input=x, answer=ans)])
            return value_last_step_prompt.format(input=x, answer=ans)
        current_numbers = get_current_numbers(y)
        return value_prompt.format(input=current_numbers)
    
    @staticmethod
    def value_outputs_unwrap(x: str, y: str, value_outputs: list) -> float:
        if len(y.strip().split('\n')) == 4 and 'answer' not in y.lower():
            return 0
        value_names = [_.split('\n')[-1] for _ in value_outputs]
        value_map = {'impossible': 0.001, 'likely': 1, 'sure': 20}  # TODO: ad hoc
        value = sum(value * value_names.count(name) for name, value in value_map.items())
        return value