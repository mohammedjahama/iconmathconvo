import json
from typing import List, Dict, Union
import random

class Skill:
    def __init__(self, name_ar: str, description_ar: str):
        self.name_ar = name_ar
        self.description_ar = description_ar
        self.questions = []

class Question:
    def __init__(self, text_ar: str, correct_answer: str, choices: List[str], 
                 feedback_correct_ar: str, feedback_incorrect_ar: str, 
                 shape_meta: str = None):
        self.text_ar = text_ar
        self.correct_answer = correct_answer
        self.choices = choices
        self.feedback_correct_ar = feedback_correct_ar
        self.feedback_incorrect_ar = feedback_incorrect_ar
        self.shape_meta = shape_meta

class Lesson:
    def __init__(self, title_ar: str, grade: int, unit: int):
        self.title_ar = title_ar
        self.grade = grade
        self.unit = unit
        self.skills: List[Skill] = []
        self.dialogue_ar = ""
        
    def add_skill(self, skill: Skill):
        self.skills.append(skill)
        
    def set_dialogue(self, dialogue_ar: str):
        self.dialogue_ar = dialogue_ar
        
    def generate_exam(self) -> List[Question]:
        exam_questions = []
        for skill in self.skills:
            # Select 2-3 questions per skill
            num_questions = random.randint(2, 3)
            if skill.questions:
                selected = random.sample(skill.questions, min(num_questions, len(skill.questions)))
                exam_questions.extend(selected)
        return exam_questions

    def grade_exam(self, answers: Dict[int, str], questions: List[Question]) -> Dict:
        total_questions = len(questions)
        correct_count = 0
        feedback = []
        
        for i, (question, answer) in enumerate(zip(questions, answers.values())):
            is_correct = answer == question.correct_answer
            correct_count += 1 if is_correct else 0
            
            feedback.append({
                'question_num': i + 1,
                'is_correct': is_correct,
                'feedback': question.feedback_correct_ar if is_correct else question.feedback_incorrect_ar
            })
        
        score = (correct_count / total_questions) * 100
        
        return {
            'score': score,
            'correct_count': correct_count,
            'total_questions': total_questions,
            'feedback': feedback
        }

def create_shape_meta(shape_type: str, dimensions: Dict[str, float] = None) -> str:
    """
    Create meta description for shapes that need to be drawn
    Example: <shape type="square" width="5cm"/>
    """
    if dimensions:
        dims = ' '.join([f'{k}="{v}"' for k, v in dimensions.items()])
        return f'<shape type="{shape_type}" {dims}/>'
    return f'<shape type="{shape_type}"/>'

# Example usage:
def create_sample_lesson():
    # Create a sample math lesson about squares
    lesson = Lesson(
        title_ar="المربعات",  # Squares
        grade=3,
        unit=1
    )
    
    # Add a skill
    skill = Skill(
        name_ar="تحديد خصائص المربع",  # Identifying square properties
        description_ar="القدرة على تحديد خصائص المربع من حيث الأضلاع والزوايا"  # Ability to identify square properties in terms of sides and angles
    )
    
    # Create a question with a shape
    shape_meta = create_shape_meta("square", {"width": "5cm"})
    question = Question(
        text_ar="كم عدد أضلاع المربع؟",  # How many sides does a square have?
        correct_answer="4",
        choices=["3", "4", "5", "6"],
        feedback_correct_ar="أحسنت! المربع له 4 أضلاع متساوية.",  # Excellent! A square has 4 equal sides.
        feedback_incorrect_ar="حاول مرة أخرى. المربع له 4 أضلاع متساوية.",  # Try again. A square has 4 equal sides.
        shape_meta=shape_meta
    )
    
    skill.questions.append(question)
    lesson.add_skill(skill)
    
    # Set the dialogue
    lesson.set_dialogue("""
    المعلم: اليوم سنتعلم عن المربعات.
    الطالب: ما هو المربع؟
    المعلم: المربع هو شكل هندسي له أربعة أضلاع متساوية وأربع زوايا قائمة.
    الطالب: كيف نعرف أن الزوايا قائمة؟
    المعلم: الزاوية القائمة تساوي 90 درجة، مثل الزاوية في ركن الورقة.
    """)
    
    return lesson

if __name__ == "__main__":
    # Create and test a sample lesson
    lesson = create_sample_lesson()
    
    # Generate an exam
    exam_questions = lesson.generate_exam()
    
    # Simulate student answers
    student_answers = {0: "4"}  # Correct answer for the first question
    
    # Grade the exam
    results = lesson.grade_exam(student_answers, exam_questions)
    
    # Print results
    print(f"Score: {results['score']}%")
    for fb in results['feedback']:
        print(f"Question {fb['question_num']}: {'Correct' if fb['is_correct'] else 'Incorrect'}")
        print(f"Feedback: {fb['feedback']}")
