from services.classifier import classify_email

result = classify_email(
    "Resume Submission",
    "Hello, please find my resume attached."
)

print(result)