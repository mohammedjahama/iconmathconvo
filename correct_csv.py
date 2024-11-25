import csv
import codecs

def correct_answertext(row, corrections):
    question_number = int(row['Id'])
    if question_number in corrections:
        row['AnswerText'] = corrections[question_number]
    return row

corrections = {
    # ... (keep the existing corrections dictionary unchanged)
}

input_file = 'outputquestionsg32.csv'
output_file = 'outputquestionsg32_corrected.csv'

with codecs.open(input_file, 'r', encoding='utf-8-sig') as infile, \
     codecs.open(output_file, 'w', encoding='utf-8-sig') as outfile:
    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames

    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    for row in reader:
        corrected_row = correct_answertext(row, corrections)
        writer.writerow(corrected_row)

print(f"Corrected CSV file has been created: {output_file}")