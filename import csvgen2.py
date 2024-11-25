import csv
import os
from collections import defaultdict
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # Use environment variable

# Function to generate detailed feedback
def generate_feedback(concept_name, answer_text):
    prompt = (
        f"Based on the concept '{concept_name}' and the answer '{answer_text}', "
        "provide detailed feedback in 100 words or less."
    )

    response = client.chat.completions.create(model="gpt-4",  # or "gpt-3.5-turbo"
    messages=[{"role": "user", "content": prompt}])

    feedback = response.choices[0].message.content
    return feedback

def process_csv(input_csv_path, output_csv_path):
    # Dictionary to hold concept data
    concepts_dict = defaultdict(lambda: defaultdict(lambda: {'answers': [], 'correct_answer': None, 'question': None}))

    # Read the input CSV file
    with open(input_csv_path, mode='r', newline='') as infile:
        reader = csv.DictReader(infile, delimiter=',')  # Change delimiter to comma
        for row in reader:
            # Strip whitespace from keys
            row = {k.strip(): v for k, v in row.items()}  # Strip whitespace from keys
            print(row.keys())  # Debugging line to see available keys
            concept_name = row['ConceptName']  # This line may raise KeyError
            question_text = row['Question']  # Use 'Question' instead of 'QuestionName'
            answer_text = row['AnswerText']
            correct_answer = row.get('CorrectAnswer', '')  # Get the 'CorrectAnswer' field if available

            # Clean up the correct answer if it's a string
            if isinstance(correct_answer, str):  # Check if it's a string
                correct_answer = correct_answer.replace('<p>', '').replace('</p>', '').strip()
            else:
                # Handle the case where correct_answer is not a string
                correct_answer = ''  # or some default value

            # Store the correct answer separately if it exists
            if answer_text.lower() == 'yes' or correct_answer:  # Adjusted logic to check answer_text and correct_answer
                concepts_dict[concept_name]['correct_answer'] = correct_answer or answer_text
            else:
                if 'answers' not in concepts_dict[concept_name]:
                    concepts_dict[concept_name]['answers'] = []  # Initialize as a list
                concepts_dict[concept_name]['answers'].append(f"Wrong:{answer_text}")

            # Store the question text
            concepts_dict[concept_name]['question'] = question_text  # Store question text directly

    # Write the processed data to a new CSV file
    with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['ConceptName', 'Question', 'AnswerText', 'Correct', 'Feedback']  # Removed 'QuestionName'
        csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        csv_writer.writeheader()

        for concept_name, data in concepts_dict.items():  # Adjusted loop to reflect changes
            # Format the answer text
            answer_texts = []
            if data['correct_answer']:
                answer_texts.append(f"Right:{data['correct_answer']}")
            answer_texts.extend(data['answers'])

            # Combine all answers into the required format
            all_answers = ','.join(answer_texts)

            # Generate feedback based on the concept name, question, and all answers
            feedback = generate_feedback(concept_name, f"{data['question']} {all_answers}")  # Include question in feedback

            # Write the row to the output CSV
            csv_writer.writerow({
                'ConceptName': concept_name,
                'Question': data['question'],  # Write the merged question text
                'AnswerText': all_answers,
                'Correct': 'yes' if data['correct_answer'] else 'no',  # This line may need to be adjusted
                'Feedback': feedback  # Add feedback to the row
            })

# Example usage
if __name__ == "__main__":
    print("Starting the script...")
    input_csv_path = '/Users/monova/scrape/outputquestionsg32.csv'  # Update with your input CSV file path
    output_csv_path = '/Users/monova/scrape/outputquestionsg32feedback.csv'  # Update with your desired output CSV file path
    process_csv(input_csv_path, output_csv_path)
    print("Script finished.")
