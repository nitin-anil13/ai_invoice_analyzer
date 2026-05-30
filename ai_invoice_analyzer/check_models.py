from groq import Groq

client = Groq(api_key="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")

models = client.models.list()

for m in models.data:
    print(m.id)