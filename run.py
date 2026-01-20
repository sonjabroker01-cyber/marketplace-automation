import os
from openai import OpenAI

client = OpenAI()

ORDERS_DIR = "orders"
OUTPUT_DIR = "outputs"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def optimize_resume(text):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a professional resume writer and ATS expert."},
            {"role": "user", "content": f"""
Rewrite this resume to be:
- Professional
- ATS-friendly
- Results-focused
- Clean formatting

Resume:
{text}
"""}
        ]
    )
    return response.choices[0].message.content

def generate_cover_letter(resume_text):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a professional career coach."},
            {"role": "user", "content": f"""
Write a concise, professional cover letter based on this resume:

{resume_text}
"""}
        ]
    )
    return response.choices[0].message.content

for filename in os.listdir(ORDERS_DIR):
    if not filename.endswith(".txt"):
        continue

    client_name = filename.replace("_resume.txt", "")
    print(f"Processing {client_name}...")

    with open(os.path.join(ORDERS_DIR, filename), "r", encoding="utf-8") as f:
        resume_text = f.read()

    optimized_resume = optimize_resume(resume_text)
    cover_letter = generate_cover_letter(resume_text)

    with open(f"{OUTPUT_DIR}/{client_name}_resume_optimized.txt", "w", encoding="utf-8") as f:
        f.write(optimized_resume)

    with open(f"{OUTPUT_DIR}/{client_name}_cover_letter.txt", "w", encoding="utf-8") as f:
        f.write(cover_letter)

print("✅ All orders completed!")
