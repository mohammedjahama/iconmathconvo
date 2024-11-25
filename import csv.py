import csv
from collections import defaultdict
from openai import OpenAI

client = OpenAI(api_key="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")  # Import the OpenAI library

# Directly set the OpenAI API key (not recommended for production)
  # Replace with your actual API key

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
            question_name = row['QuestionName']
            answer_text = row['AnswerText']
            correct = row['Correct']
            question_text = row['Question']  # Capture the question text

            # Store the correct answer separately
            if correct.lower() == 'yes':  # Use lower() to handle case sensitivity
                concepts_dict[concept_name][question_name]['correct_answer'] = answer_text
            else:
                concepts_dict[concept_name][question_name]['answers'].append(f"Wrong:{answer_text}")

            # Store the question text
            if concepts_dict[concept_name][question_name]['question'] is None:
                concepts_dict[concept_name][question_name]['question'] = question_text

    # Write the processed data to a new CSV file
    with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['ConceptName', 'QuestionName', 'Question', 'AnswerText', 'Correct', 'Feedback']  # Added 'Feedback'
        csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        csv_writer.writeheader()

        for concept_name, questions in concepts_dict.items():
            for question_name, data in questions.items():
                # Format the answer text
                answer_texts = []
                if data['correct_answer']:
                    answer_texts.append(f"Right:{data['correct_answer']}")
                answer_texts.extend(data['answers'])

                # Combine all answers into the required format
                all_answers = ','.join(answer_texts)

                # Check if the answer contains HTML and clean it if necessary
                if "Right:" in all_answers:
                    # Extract the correct answer without HTML tags
                    correct_answer = data['correct_answer'].replace('<p>', '').replace('</p>', '').strip()
                else:
                    correct_answer = None

                # Generate feedback based on the concept name and correct answer
                feedback = generate_feedback(concept_name, all_answers)  # Generate feedback

                # Write the row to the output CSV
                csv_writer.writerow({
                    'ConceptName': concept_name,
                    'QuestionName': question_name,
                    'Question': data['question'],  # Write the merged question text
                    'AnswerText': all_answers,
                    'Correct': 'yes' if correct_answer else 'no',
                    'Feedback': feedback  # Add feedback to the row
                })

# Example usage
if __name__ == "__main__":
    print("Starting the script...")
    input_csv_path = '/Users/monova/scrape/outputquestionsg32.csv'  # Update with your input CSV file path
    output_csv_path = '/Users/monova/scrape/outputquestionsg32feedback.csv'  # Update with your desired output CSV file path
    process_csv(input_csv_path, output_csv_path)
    print("Script finished.")
