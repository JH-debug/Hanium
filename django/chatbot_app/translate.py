import boto3

translate = boto3.client('translate')
result = translate.translate_text(Text="I love you so much",
                                  SourceLanguageCode="auto",
                                  TargetLanguageCode="ko")
translated = result["TranslatedText"]
print(translated)
