import re

# 讀取文字檔
with open("RegularExpression練習文本.txt", "r", encoding="utf-8") as f:
    text = f.read()

# 1
years = re.findall(r"\b\d{4}\b", text)
print("(1) ", years)

# 2
percentages = re.findall(r"\b\d+(?:\.\d+)?%", text)
print("(2) ", percentages)

# 3
comma_nums = re.findall(r"\b\d{1,3}(?:,\d{3})+\b", text)
print("(3) ", comma_nums)

# 4
money_units = re.findall(r"\$\s*\d+(?:\.\d+)?\s*(?:million|billion|trillion)", text, flags=re.IGNORECASE)
print("(4) ", money_units)

# 5
sixg = re.findall(r"\b6[Gg]\b", text)
print("(5) ", sixg)

# 6
stocks = re.findall(r"\(([A-Z]{1,6})\)", text)
print("(6) ", stocks)

# 7
dashes = re.findall(r"\b[A-Z][^—–]+[—–][^。！？]*", text)
print("(7) ", dashes,"\n")

# 8
in_places = re.findall(r"\b[Ii]n\s+[A-Z][a-z]+", text)
print("(8) ", in_places,"\n")


'''
Find_Nvidia = re.findall(r"(?:\b\w+\b\s+){0,3}\bNvidia\b(?:\'s|'s|s)?(?:\s+\b\w+\b){0,3}", text)
print("9.Nvidia:",Find_Nvidia)
'''