from openai import OpenAI

openai = OpenAI(
    api_key="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"
)

response = openai.images.generate(
    prompt='happy labrador',
    n=1,
    size="1024x1024"
)

image_url = response.data[0].url

print(image_url)