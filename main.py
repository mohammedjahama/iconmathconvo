import json
import os
from typing import Dict, List
from dialogue_skill_generator import DialogueSkillGenerator
from exam_generator import ExamGenerator, ExamGrader
from validate_llm_output import process_llm_output

class MathLessonSystem:
    def __init__(self):
        self.dialogue_generator = DialogueSkillGenerator()
        self.exam_generator = ExamGenerator()
        
        # Create output directories if they don't exist
        os.makedirs('generated_lessons', exist_ok=True)
        os.makedirs('generated_exams', exist_ok=True)
        os.makedirs('student_results', exist_ok=True)
    
    def generate_lesson_content(self, topic: str, grade: int, unit: int) -> Dict:
        """
        Generate complete lesson content using LLM.
        You would integrate this with your preferred LLM service.
        """
        # 1. Generate dialogue prompt
        dialogue_prompt = self.dialogue_generator.generate_lesson_dialogue(
            topic=topic,
            grade=grade,
            unit=unit
        )
        print("\n1. Generated dialogue prompt for LLM:")
        print(dialogue_prompt)
        
        # Here you would send the prompt to your LLM and get the response
        # llm_response = your_llm.generate(dialogue_prompt)
        
        # For demonstration, we'll use sample content
        sample_dialogue = {
            "title_ar": f"درس {topic}",
            "grade": grade,
            "unit": unit,
            "dialogue_ar": {
                "exchanges": [
                    {
                        "teacher": "اليوم سنتعلم عن الضرب",
                        "student": "ما هو الضرب؟"
                    }
                ]
            }
        }
        
        # 2. Extract skills
        skills_prompt = self.dialogue_generator.extract_skills_from_dialogue(sample_dialogue)
        print("\n2. Generated skills extraction prompt for LLM:")
        print(skills_prompt)
        
        # Here you would send the prompt to your LLM and get skills
        # skills_response = your_llm.generate(skills_prompt)
        
        # For demonstration, we'll use sample skills
        sample_skills = [
            {
                "name_ar": "فهم مفهوم الضرب",
                "description_ar": "القدرة على فهم الضرب كعملية تكرار الجمع",
                "difficulty": 1
            }
        ]
        
        # 3. Generate questions for each skill
        all_questions = []
        for skill in sample_skills:
            questions_prompt = self.dialogue_generator.generate_questions_for_skill(skill)
            print(f"\n3. Generated questions prompt for skill {skill['name_ar']}:")
            print(questions_prompt)
            
            # Here you would send the prompt to your LLM and get questions
            # questions_response = your_llm.generate(questions_prompt)
            
            # For demonstration, we'll use sample questions
            sample_questions = [
                {
                    "text_ar": "كم ناتج ضرب ٤ × ٣؟",
                    "type": "multiple_choice",
                    "choices": ["٨", "١٢", "١٠", "١٥"],
                    "correct_answer": "١٢",
                    "feedback_correct_ar": "أحسنت! ٤ × ٣ = ١٢",
                    "feedback_incorrect_ar": "حاول مرة أخرى. فكر في جمع الرقم ٣ أربع مرات",
                    "difficulty": 1
                }
            ]
            all_questions.extend(sample_questions)
        
        # 4. Combine everything into lesson content
        lesson_content = {
            **sample_dialogue,
            "skills": [
                {
                    **skill,
                    "questions": [q for q in all_questions if q["difficulty"] == skill["difficulty"]]
                }
                for skill in sample_skills
            ]
        }
        
        return lesson_content
    
    def save_lesson_content(self, content: Dict, topic: str, grade: int):
        """Save generated lesson content to file"""
        filename = f"generated_lessons/lesson_{grade}_{topic.replace(' ', '_')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(content, f, ensure_ascii=False, indent=2)
        return filename
    
    def generate_and_save_exam(self, lesson_file: str) -> str:
        """Generate exam from lesson content and save it"""
        # Load lesson content and generate exam
        self.exam_generator.load_lesson_content(lesson_file)
        exam = self.exam_generator.generate_exam(os.path.basename(lesson_file))
        
        # Save exam
        exam_file = f"generated_exams/exam_{exam.exam_id}.json"
        with open(exam_file, 'w', encoding='utf-8') as f:
            json.dump({
                "exam_id": exam.exam_id,
                "title_ar": exam.title_ar,
                "lesson_id": exam.lesson_id,
                "questions": [
                    {
                        "question_id": q.question_id,
                        "skill_id": q.skill_id,
                        "text_ar": q.text_ar,
                        "type": q.type,
                        "choices": q.choices,
                        "shape_meta": q.shape_meta
                    }
                    for q in exam.questions
                ]
            }, f, ensure_ascii=False, indent=2)
        
        return exam_file
    
    def grade_exam_and_save_results(self, exam_file: str, student_answers: Dict[str, str], student_id: str):
        """Grade exam and save student results"""
        # Load exam
        with open(exam_file, 'r', encoding='utf-8') as f:
            exam_data = json.load(f)
        
        # Get original lesson file from exam ID
        lesson_id = exam_data['lesson_id']
        lesson_file = f"generated_lessons/{lesson_id}"
        
        # Load lesson content for grading
        self.exam_generator.load_lesson_content(lesson_file)
        
        # Create grader and grade exam
        grader = ExamGrader(self.exam_generator.skills)
        results = grader.grade_exam(self.exam_generator.generate_exam(lesson_id), student_answers)
        
        # Save results
        results_file = f"student_results/student_{student_id}_exam_{exam_data['exam_id']}.json"
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        return results_file

def main():
    """Example usage of the complete system"""
    system = MathLessonSystem()
    
    # 1. Generate lesson content
    print("Generating lesson content...")
    lesson_content = system.generate_lesson_content(
        topic="multiplication",
        grade=3,
        unit=1
    )
    
    # 2. Save lesson content
    print("\nSaving lesson content...")
    lesson_file = system.save_lesson_content(lesson_content, "multiplication", 3)
    print(f"Lesson saved to: {lesson_file}")
    
    # 3. Generate exam
    print("\nGenerating exam...")
    exam_file = system.generate_and_save_exam(lesson_file)
    print(f"Exam saved to: {exam_file}")
    
    # 4. Simulate student taking exam
    print("\nSimulating student answers...")
    student_answers = {
        "question_1": "١٢",  # Correct answer for sample question
    }
    
    # 5. Grade exam and save results
    print("\nGrading exam...")
    results_file = system.grade_exam_and_save_results(exam_file, student_answers, "student_001")
    print(f"Results saved to: {results_file}")
    
    # 6. Display results
    with open(results_file, 'r', encoding='utf-8') as f:
        results = json.load(f)
    
    print("\nExam Results:")
    print(f"Total Score: {results['score_percentage']}%")
    print("\nSkill Performance:")
    for skill_id, perf in results["skill_performance"].items():
        print(f"\n{perf['name_ar']}:")
        print(f"Percentage: {perf['percentage']}%")
        print(f"Feedback: {perf['feedback_ar']}")

if __name__ == "__main__":
    main()
