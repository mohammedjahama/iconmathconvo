import csv
from difflib import get_close_matches

def load_csv(file_path):
    with open(file_path, 'r') as f:
        return list(csv.DictReader(f))

def find_best_match(concept, lessons):
    lesson_names = [lesson['Lesson'] for lesson in lessons]
    matches = get_close_matches(concept, lesson_names, n=1, cutoff=0.6)
    return matches[0] if matches else None

# Load data
questions = load_csv('questions grade 3, corrected, might need more.csv')
lessons = load_csv('lessons_grade3, full list, not full questions associated.csv')

# Create mapping
concept_lesson_mapping = {}
for question in questions:
    concept = question['ConceptName']
    if concept not in concept_lesson_mapping:
        best_match = find_best_match(concept, lessons)
        concept_lesson_mapping[concept] = best_match

# Save mapping
with open('auto_generated_concept_lesson_mapping.py', 'w') as f:
    f.write('concept_lesson_mapping = ' + repr(concept_lesson_mapping))

# Print unmapped concepts for manual review
unmapped = [concept for concept, lesson in concept_lesson_mapping.items() if lesson is None]
print("Concepts that need manual mapping:", unmapped)