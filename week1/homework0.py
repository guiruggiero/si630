# SI 630, Winter 2020 - homework 0
# Developed by Gui Ruggiero

from bs4 import BeautifulSoup
import re
import csv

# Import file contents
i = 0
websites_p = []
f = open("W20_webpages.txt", "r")
for line in f:
    # print(line)
    
    # websites.append(line)
    # print(websites[i])

    # website_p = BeautifulSoup(line, "html.parser").find("p").text
    # print(website_p)

    websites_p.append(BeautifulSoup(line, "html.parser").find("p").text)
    # print(websites_p[i])

    # Iteration limiter for testing
    i += 1
    # if i == 10:
    #     break

print("i =", i)
f.close()

# Extracting emails
emails = []
for line in websites_p:
    match = re.search(r'[\w\.-]+@[\w\.-]+', line) #flag
    if match:
        # print(match.group(0))
        emails.append(match.group(0))
    else:
        emails.append("None")

# Exporting CSV
j = 0
with open("email-outputs.csv", "w") as f:
    for line in emails:
        # print(line)
        f.write(line)
        j += 1
        if j != i:
            f.write("\n")

print("j =", j)
f.close()