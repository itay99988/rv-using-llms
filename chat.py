import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")


class Chat:
    def __init__(self, model="gpt-4", temperature=0.4, max_tokens=1024):
        self.QUERY_LIMIT = 20
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.msg_context = []

    def reset_history(self):
        self.msg_context = []

    def pop_history(self, items_count):
        for _ in range(items_count):
            self.msg_context.pop()

    def new_message(self, msg):
        self.msg_context.append({
          "role": "user",
          "content": msg
        })
        try:
            full_response = openai.ChatCompletion.create(
              model=self.model,
              messages=self.msg_context,
              temperature=self.temperature,
              max_tokens=self.max_tokens,
              top_p=1,
              frequency_penalty=0,
              presence_penalty=0
            )
        except:
            err = "Could not send the message."
            return err

        response = full_response['choices'][0]["message"]["content"]
        self.add_assistant_msg(response)
        return response

    def add_assistant_msg(self, ass_msg):
        self.msg_context.append({
          "role": "assistant",
          "content": ass_msg
        })


class OldChat:
    def __init__(self, model="text-davinci-003", temperature=0.5, max_tokens=1024):
        self.QUERY_LIMIT = 20
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.msg_context = []

    def reset_history(self):
        self.msg_context = []

    def pop_history(self, items_count):
        for _ in range(items_count):
            self.msg_context.pop()

    def concat_chat(self):
        return '\n\n'.join(self.msg_context)

    def new_message(self, msg):
        self.msg_context.append(msg)
        try:
            full_response = openai.Completion.create(
                model="text-davinci-003",
                prompt=self.concat_chat(),
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0
            )
        except:
            err = "Could not send the message."
            return err

        response = full_response['choices'][0]["text"]
        self.msg_context.append(response)
        return response
