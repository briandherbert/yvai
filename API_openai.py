import openai

# export OPENAI_API_KEY=

def getChatGPTAnswer(
    prompt,  
    model="gpt-3.5-turbo",
    max_tokens = 30,
    system_prompt = None
):
    messages = [{"role": "user", "content": prompt}]

    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        max_tokens = int(max_tokens)
        ) 
    answer = None  
    print(f'got answer {response}')
    try:
        answer = response["choices"][0]["message"]["content"].strip()  
    except:
        pass
    return answer