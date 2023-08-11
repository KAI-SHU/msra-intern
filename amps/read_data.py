def read(fname):
    question = ""
    curr_section = ""
    answers = []
    with open(fname, 'r') as fp:       
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
    return question, len(curr_section.split("\n \n"))

print(read("/home/v-kailaisun/amps/mathematica/calculus/derivatives_w_steps/0.txt"))
