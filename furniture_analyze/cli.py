import argparse
from .process_plan import process_plan

def main():
    parser = argparse.ArgumentParser(description="Process furniture plan files.")
    parser.add_argument("filename", type=str, help="Path to the plan file.")
    args = parser.parse_args()

    # Read in the plan from the text file as a str
    try:
        with open(args.filename, "r") as file:
            input_str = file.read()
    except FileNotFoundError:
        print("Error: File not found.")
        return
    except Exception as e:
        print("Error:", e)
        return

    # Process the plan using process_plan function
    rooms = process_plan(input_str)
    for room in rooms:
        print(room)

if __name__ == "__main__":
    main()
