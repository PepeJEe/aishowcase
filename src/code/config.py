import dotenv

class Settings():
    env_file = ".env"
    SYSTEM_PROMPT: str = "You are a computer for supply chain risk and escalation alarm. You output the necessary details and info based on what you will receive from the user."

    def __init__(self):
        loaded_conf = dotenv.dotenv_values(self.env_file)
        self.ollama_host = loaded_conf.get('OLLAMA_HOST', "https://ollama.pepevapp.com" )
        self.model = loaded_conf.get('MODEL', "llama3.2:3b")
        self.max_tokens = loaded_conf.get('MAX_TOKENS', 2048)
        self.system_prompt = loaded_conf.get('SYSTEM_PROMPT', self.SYSTEM_PROMPT)