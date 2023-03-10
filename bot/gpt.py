import openai
import json

with open('api.key', 'r') as f:
    openai.api_key = f.read()

# The Personality-File is just a small description to tell how ChatGPT should act
with open('personality.txt', 'r') as f:
    personality = f.read()

def get_history(channelID):
    try:
        f = open('{}.json'.format(channelID))
        data = json.load(f)
        return data
    except FileNotFoundError:
        with open('{}.json'.format(channelID), 'w') as f:
            f.write("""[{"role": "system", "content": "%s"}]"""%personality)
def get_message_answer(user, message, channelID):
    history = get_history(channelID)
    add_to_history(channelID, {"role": "user", "content": str(user) + " " + str(message)})
    history = get_history(channelID)
    chat = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=history
    )
    answer = chat['choices'][0]['message']['content']
    print(chat['usage']['total_tokens'])
    add_to_history(channelID, {"role": "assistant", "content": answer})
    return answer

def add_to_history(channelID, json_string):
    with open('{}.json'.format(channelID), 'r+') as file:
        file_data = json.load(file)
        file_data.append(json_string)
        file.seek(0)
        json.dump(file_data, file, indent=4)

