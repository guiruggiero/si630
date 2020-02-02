# SI 630, Winter 2020 - homework 0
# Developed by Gui Ruggiero

from bs4 import BeautifulSoup
import re

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
with open("email-no_match.txt", "w") as f:
    for line in websites_p:
        # match = re.search(r'[\w\.-]+@[\w\.-]+', line)
        match = re.search(r'([a-zA-Z0-9_\-\.\_]{1,64})@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})', line)
        if match:
            # print(match.group(0))
            emails.append(match.group(0))
        else:
            match = re.search(r'([a-zA-Z0-9_\-\.\_]+)(\s@?\[?\/?([aA][tT])?\]?\/?\s)([a-zA-Z0-9_\-\.]+)(\s\.?\[?\/?([dD][oO][tT])?\]?\/?\s)([a-zA-Z]{2,5})', line)
            if match:
                # text = match.group(0)
                text = match.group(1) + "@" + match.group(4) + "." + match.group(7)
                emails.append(text)
            else:
                # text = "***** REVIEW - " + line
                # emails.append(text)
                emails.append("None")
                f.write(line)
                f.write("\n")

f.close()

# Exporting CSV
j = 0
with open("email-outputs.csv", "w") as f:
    f.write("Id,Category")
    f.write("\n")
    for line in emails:
        # print(line)
        f.write(str(j))
        f.write(",")
        f.write(line)
        j += 1
        if j != i:
            f.write("\n")

print("j =", j)
f.close()