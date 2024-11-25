import csv
from updated_concept_lesson_mapping import updated_concept_lesson_mapping

# Read the questions CSV file
input_file = 'questions grade 3, corrected, might need more.csv'
output_file = 'updated_questions_grade3.csv'

with open(input_file, 'r', newline='', encoding='utf-8') as infile, open(output_file, 'w', newline='', encoding='utf-8') as outfile:
    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames

    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    for row in reader:
        old_concept = row['ConceptName']
        if old_concept in updated_concept_lesson_mapping:
            row['ConceptName'] = updated_concept_lesson_mapping[old_concept]
        writer.writerow(row)

print(f"Updated CSV file has been created: {output_file}")