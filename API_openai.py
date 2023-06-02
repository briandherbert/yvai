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
        max_tokens = int(max_tokens),
        stream = True
        ) 
    answer = None  
    print(f'got answer {response}')
    try:
        answer = response["choices"][0]["message"]["content"].strip()  
    except:
        pass
    return answer

# response = getChatGPTAnswer("who are you?")
# print(str(response))

def streamResponse(prompt):
    for chunk in openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{
            "role": "user",
            "content": prompt
        }],
        stream=True,
    ):
        content = chunk["choices"][0].get("delta", {}).get("content")
        if content is not None:
            print(content, end='')