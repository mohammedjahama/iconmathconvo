import csv
from difflib import SequenceMatcher

def read_csv(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def find_best_match(concept_name, lessons):
    best_match = None
    best_ratio = 0
    for lesson in lessons:
        ratio = SequenceMatcher(None, concept_name.lower(), lesson['Lesson'].lower()).ratio()
        if ratio > best_ratio:
            best_ratio = ratio
            best_match = lesson
    return best_match if best_ratio > 0.6 else None

def associate_lessons_questions(lessons_file, questions_file):
    try:
        lessons = read_csv(lessons_file)
        questions = read_csv(questions_file)
    except FileNotFoundError as e:
        print(f"Error: File not found - {e}")
        return None
    except csv.Error as e:
        print(f"Error reading CSV file: {e}")
        return None

    lessons_with_questions = {}
    
    for question in questions:
        try:
            concept_name = question['ConceptName']
            best_match = find_best_match(concept_name, lessons)
            if best_match:
                lesson_id = best_match['Id']
                if lesson_id not in lessons_with_questions:
                    lessons_with_questions[lesson_id] = {
                        'lesson_name': best_match['Lesson'],
                        'questions': []
                    }
                lessons_with_questions[lesson_id]['questions'].append(question)
        except KeyError as e:
            print(f"Error: Missing column in questions CSV - {e}")
            return None

    return lessons_with_questions

def write_associated_data(lessons_with_questions, output_file):
    if not lessons_with_questions:
        print("No data to write.")
        return

    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Lesson ID', 'Lesson Name', 'Question ID', 'Concept Name', 'Question', 'Answer'])
        
        for lesson_id, data in lessons_with_questions.items():
            lesson_name = data['lesson_name']
            for question in data['questions']:
                writer.writerow([
                    lesson_id,
                    lesson_name,
                    question['Id'],
                    question['ConceptName'],
                    question['Question'],
                    question['AnswerText']
                ])

if __name__ == "__main__":
    lessons_file = 'lessonsgrade3 - lessons (8).csv'
    questions_file = 'outputquestionsg32_corrected.csv'
    output_file = 'lessons_questions_associated.csv'
    
    lessons_with_questions = associate_lessons_questions(lessons_file, questions_file)
    if lessons_with_questions:
        write_associated_data(lessons_with_questions, output_file)
        print(f"Associated data has been written to {output_file}")
    else:
        print("Failed to associate lessons with questions.")