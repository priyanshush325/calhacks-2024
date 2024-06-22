def generatePrompt(promptFilePath, parameters):
    with open(promptFilePath, 'r') as file:
        prompt = file.read()

        i = 0
        for item in parameters:
            paramTag = "[PARAM" + str(i) + "]"
            prompt = prompt.replace(paramTag, item)
            i += 1

        return prompt


def requestGPT(client, model, question):
    chat_completion = client.chat.completions.create(
        model=model,
        seed=69,
        response_format={"type": "json_object"},
        messages=[{"role": "user", "content": question}],
    )
    return chat_completion.choices[0].message.content
