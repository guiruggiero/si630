def main():
    print("Hello. How are you feeling today?")

    while True:
        statement = raw_input("> ")
        print(analyze(statement))

        if statement == "quit":
            break

def analyze(statement):
    statement = statement.rstrip(".!") # remove punch
    for pattern, responses in psychobabble:
        match = re.match(pattern, statement)
        if match:
            response = random.choice(responses)
            return response.format(
                *[reflect(g) for g in match.groups()])

def reflect(fragment):
    tokens = fragment.lower().split()
    for i, token in enumerate(tokens):
        if token in reflections:
            tokens[i] = reflections[token]
    return ' '.join(tokens)