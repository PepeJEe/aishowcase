import dotenv

class Settings():
    env_file = ".env"
    SYSTEM_PROMPT: str = "You are computer supply chain risk and escalation alarm. You output the necessary details and info based on what you will receive from the user."

    def __init__(self):
        loaded_conf = dotenv.dotenv_values(self.env_file)
        self.ollama_host = loaded_conf.get('ollamaHost', "https://ollama.pepevapp.com" )
        self.model = loaded_conf.get('defaultModel', "qwen2.5:1.5b")
        print(f'LOADED MODEL: {self.model}')
        self.max_tokens = loaded_conf.get('maxTokens', 2048)
        self.system_prompt = loaded_conf.get('systemPrompt', self.SYSTEM_PROMPT)