import json
import random
from typing import Dict, List, Tuple
from dataclasses import dataclass

@dataclass
class Question:
    question_id: str
    skill_id: str
    text_ar: str
    type: str
    choices: List[str]
    correct_answer: str
    feedback_correct_ar: str
    feedback_incorrect_ar: str
    difficulty: int
    shape_meta: str = None

@dataclass
class Skill:
    skill_id: str
    name_ar: str
    description_ar: str
    questions: List[Question]

@dataclass
class Exam:
    exam_id: str
    title_ar: str
    lesson_id: str
    questions: List[Question]
    skill_coverage: Dict[str, int]  # skill_id -> question_count

class ExamGenerator:
    def __init__(self):
        self.question_bank = {}  # skill_id -> List[Question]
        self.skills = {}  # skill_id -> Skill
    
    def load_lesson_content(self, lesson_file: str):
        """Load questions and skills from a lesson file"""
        with open(lesson_file, 'r', encoding='utf-8') as f:
            lesson_data = json.load(f)
            
        for skill_data in lesson_data['skills']:
            skill_id = skill_data['name_ar']  # Using name_ar as ID for simplicity
            
            # Create skill object
            skill = Skill(
                skill_id=skill_id,
                name_ar=skill_data['name_ar'],
                description_ar=skill_data['description_ar'],
                questions=[]
            )
            
            # Process questions
            for q_data in skill_data['questions']:
                question = Question(
                    question_id=f"{skill_id}_{len(skill.questions)}",
                    skill_id=skill_id,
                    text_ar=q_data['text_ar'],
                    type=q_data.get('type', 'multiple_choice'),
                    choices=q_data['choices'],
                    correct_answer=q_data['correct_answer'],
                    feedback_correct_ar=q_data['feedback_correct_ar'],
                    feedback_incorrect_ar=q_data['feedback_incorrect_ar'],
                    difficulty=q_data.get('difficulty', 1),
                    shape_meta=q_data.get('shape_meta')
                )
                skill.questions.append(question)
            
            self.skills[skill_id] = skill
            self.question_bank[skill_id] = skill.questions
    
    def generate_exam(self, lesson_id: str, questions_per_skill: int = 2) -> Exam:
        """Generate a balanced exam from the question bank"""
        selected_questions = []
        skill_coverage = {}
        
        for skill_id, questions in self.question_bank.items():
            # Select questions for this skill
            skill_questions = random.sample(
                questions,
                min(questions_per_skill, len(questions))
            )
            selected_questions.extend(skill_questions)
            skill_coverage[skill_id] = len(skill_questions)
        
        # Shuffle questions
        random.shuffle(selected_questions)
        
        return Exam(
            exam_id=f"exam_{lesson_id}_{random.randint(1000, 9999)}",
            title_ar=f"اختبار الدرس {lesson_id}",
            lesson_id=lesson_id,
            questions=selected_questions,
            skill_coverage=skill_coverage
        )

class ExamGrader:
    def __init__(self, skills: Dict[str, Skill]):
        self.skills = skills
    
    def grade_exam(self, exam: Exam, student_answers: Dict[str, str]) -> Dict:
        """Grade exam and provide detailed feedback"""
        results = {
            "total_score": 0,
            "total_questions": len(exam.questions),
            "skill_performance": {},
            "question_feedback": [],
            "recommendations": {}
        }
        
        # Initialize skill performance tracking
        for skill_id in exam.skill_coverage.keys():
            results["skill_performance"][skill_id] = {
                "correct": 0,
                "total": 0,
                "percentage": 0,
                "name_ar": self.skills[skill_id].name_ar,
                "feedback_ar": ""
            }
        
        # Grade each question and track skill performance
        for i, question in enumerate(exam.questions, 1):
            student_answer = student_answers.get(question.question_id)
            is_correct = student_answer == question.correct_answer
            
            # Update skill performance
            skill_perf = results["skill_performance"][question.skill_id]
            skill_perf["total"] += 1
            if is_correct:
                skill_perf["correct"] += 1
                results["total_score"] += 1
            
            # Add question feedback
            results["question_feedback"].append({
                "question_number": i,
                "is_correct": is_correct,
                "feedback_ar": question.feedback_correct_ar if is_correct else question.feedback_incorrect_ar,
                "skill_id": question.skill_id
            })
        
        # Calculate final statistics and generate recommendations
        for skill_id, perf in results["skill_performance"].items():
            perf["percentage"] = (perf["correct"] / perf["total"]) * 100
            
            # Generate skill-specific feedback and recommendations
            if perf["percentage"] < 60:
                perf["feedback_ar"] = f"تحتاج إلى مراجعة {self.skills[skill_id].name_ar}"
                results["recommendations"][skill_id] = {
                    "recommendation_ar": f"نوصي بمراجعة الدروس المتعلقة بـ {self.skills[skill_id].name_ar}",
                    "skill_name_ar": self.skills[skill_id].name_ar,
                    "skill_description_ar": self.skills[skill_id].description_ar
                }
            elif perf["percentage"] < 80:
                perf["feedback_ar"] = f"أداء جيد في {self.skills[skill_id].name_ar} مع مجال للتحسين"
            else:
                perf["feedback_ar"] = f"أداء ممتاز في {self.skills[skill_id].name_ar}"
        
        # Calculate overall score percentage
        results["score_percentage"] = (results["total_score"] / results["total_questions"]) * 100
        
        return results

def main():
    """Example usage of exam generation and grading"""
    # Initialize exam generator and grader
    generator = ExamGenerator()
    
    # Load sample lesson content
    generator.load_lesson_content('sample_lesson_data.json')
    
    # Generate exam
    exam = generator.generate_exam('lesson_1')
    
    # Initialize grader
    grader = ExamGrader(generator.skills)
    
    # Simulate student answers (correct answers for demonstration)
    student_answers = {
        q.question_id: q.correct_answer for q in exam.questions
    }
    
    # Grade exam
    results = grader.grade_exam(exam, student_answers)
    
    # Print results
    print("\nExam Results:")
    print(f"Total Score: {results['score_percentage']}%")
    print("\nSkill Performance:")
    for skill_id, perf in results["skill_performance"].items():
        print(f"\n{perf['name_ar']}:")
        print(f"Percentage: {perf['percentage']}%")
        print(f"Feedback: {perf['feedback_ar']}")
    
    print("\nRecommendations:")
    for skill_id, rec in results["recommendations"].items():
        print(f"\n{rec['skill_name_ar']}:")
        print(rec['recommendation_ar'])

if __name__ == "__main__":
    main()
