import json
import sys
from token_pincher.providers.claude.tokenizer import ClaudeTokenizer


def main():
    file = sys.argv[1]

    with open(file) as f:
        data = json.load(f)

    tokenizer = ClaudeTokenizer()
    usage = tokenizer.count_tokens(data["messages"])

    print(usage.total_tokens)


if __name__ == "__main__":
    main()