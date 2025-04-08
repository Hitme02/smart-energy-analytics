import subprocess
import sys

def ask_llama_stream(prompt):
    process = subprocess.Popen(
        ['ollama', 'run', 'llama3.2'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,  # line-buffered
        encoding='utf-8',  # force utf-8 encoding
    )

    # Send prompt
    process.stdin.write(prompt + '\n')
    process.stdin.close()

    # Stream output line by line
    print("Assistant:", end=' ', flush=True)
    for line in process.stdout:
        print(line, end='', flush=True)

    process.wait()

if __name__ == "__main__":
    print("💬 Smart Energy Assistant (powered by LLaMA 3.2)")
    print("Type 'exit' to quit.")
    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() in ["exit", "quit"]:
                break
            ask_llama_stream(user_input)
            print()  # for clean line break
        except KeyboardInterrupt:
            print("\nExiting.")
            sys.exit(0)
