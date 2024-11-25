import csv
from updated_concept_lesson_mapping import updated_concept_lesson_mapping

# Read the lessons CSV file
input_file = 'lessons_grade3, full list, not full questions associated.csv'
output_file = 'updated_lessons_grade3.csv'

# Create a reverse mapping from lesson names to concept names
reverse_mapping = {v: k for k, v in updated_concept_lesson_mapping.items()}

with open(input_file, 'r', newline='', encoding='utf-8') as infile, open(output_file, 'w', newline='', encoding='utf-8') as outfile:
    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames

    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    for row in reader:
        old_lesson_name = row['LessonName']
        if old_lesson_name in reverse_mapping:
            row['ConceptName'] = reverse_mapping[old_lesson_name]
        writer.writerow(row)

print(f"Updated lessons CSV file has been created: {output_file}")