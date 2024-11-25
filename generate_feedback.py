import csv
import random

def generate_feedback(concept_name, answer_text, past_concepts):
    correct_answer = next((ans.split(':')[1].strip() for ans in answer_text.split(',') if ans.startswith('Right:')), "")
    
    encouragements = [
        "Great job on tackling this concept!",
        "You're making progress in your mathematical journey!",
        "Keep up the good work and stay curious!",
        "Remember, every step forward is a victory!",
        "Your efforts in learning this concept will pay off!"
    ]
    
    improvement_tips = [
        "Try visualizing the problem to better understand it.",
        "Practice similar problems to reinforce your understanding.",
        "Don't hesitate to ask for help if you're stuck.",
        "Review the fundamental principles behind this concept.",
        "Try explaining this concept to a friend to solidify your understanding."
    ]
    
    feedback = f"Concept: {concept_name}\n"
    feedback += f"Correct answer: {correct_answer}\n\n"
    
    feedback += f"{random.choice(encouragements)} "
    
    if past_concepts:
        related_concept = random.choice(past_concepts)
        feedback += f"This concept builds upon '{related_concept}' that we covered earlier. "
        feedback += "Can you see the connection between them? "
    
    feedback += "Remember, mathematics is all about connecting ideas and building on previous knowledge. "
    
    feedback += f"\n\nIf you found this challenging, here's a tip: {random.choice(improvement_tips)} "
    feedback += "Don't get discouraged if you don't get it right away. "
    feedback += "Learning mathematics is a journey, and every step counts!"
    
    return feedback

# Read the input CSV file
with open('outputquestionsg32.csv', 'r') as input_file:
    csv_reader = csv.DictReader(input_file)
    rows = list(csv_reader)

# Add feedback to each row
past_concepts = []
for row in rows:
    row['Feedback'] = generate_feedback(row['ConceptName'], row['AnswerText'], past_concepts)
    past_concepts.append(row['ConceptName'])
    if len(past_concepts) > 5:  # Keep only the 5 most recent concepts
        past_concepts.pop(0)

# Write the output CSV file with the new feedback column
with open('generated.csv', 'w', newline='') as output_file:
    fieldnames = csv_reader.fieldnames + ['Feedback']
    csv_writer = csv.DictWriter(output_file, fieldnames=fieldnames)
    
    csv_writer.writeheader()
    csv_writer.writerows(rows)

print("Feedback generation complete. Results saved in generated.csv")