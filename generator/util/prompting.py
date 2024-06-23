import os


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

    # add the question we're asking to "./generator-logs/logs.txt"

    # if the file doesn't exist, create it
    if not os.path.exists("./generator-logs/logs.txt"):
        # create the directory
        if not os.path.exists("./generator-logs"):
            os.mkdir("./generator-logs")
        with open("./generator-logs/logs.txt", 'w') as file:
            file.write("")

    with open("./generator-logs/logs.txt", 'a') as file:
        file.write(f"=========== NEW LOG ===========\n\n\n{question}\n\n\n")

    chat_completion = client.chat.completions.create(
        model=model,
        seed=69,
        response_format={"type": "json_object"},
        messages=[{"role": "user", "content": question}],
    )

    with open("./generator-logs/logs.txt", 'a') as file:
        file.write(f"=========== GPT RESPONSE ===========\n\n\n")
        file.write(f"{chat_completion.choices[0].message.content}\n\n\n")

    return chat_completion.choices[0].message.content
