import json
import os
from typing import Dict, List, Tuple
from validate_llm_output import TerminologyValidator

class DialogueSkillGenerator:
    def __init__(self):
        self.terminology_validator = TerminologyValidator()
        self.prompt_template = self._load_prompt_template()
        
    def _load_prompt_template(self) -> str:
        """Load the LLM prompt template"""
        with open('llm_prompts.txt', 'r', encoding='utf-8') as f:
            return f.read()
    
    def generate_lesson_dialogue(self, topic: str, grade: int, unit: int) -> str:
        """
        Generate the LLM prompt for lesson dialogue generation.
        This would be used with your preferred LLM (e.g., GPT, Claude, etc.)
        """
        prompt = self.prompt_template.format(
            TOPIC=topic,
            GRADE=grade,
            UNIT=unit
        )
        return prompt
    
    def extract_skills_from_dialogue(self, dialogue_content: Dict) -> List[Dict]:
        """
        Generate a prompt to extract skills from the dialogue.
        This would be used with your preferred LLM.
        """
        skill_extraction_prompt = f"""
        Analyze this Arabic math lesson dialogue and extract the key skills being taught.
        For each skill:
        1. Provide a name in Arabic
        2. Write a detailed description in Arabic
        3. Identify the difficulty level (1-3)
        4. List key concepts covered

        The output should be in this JSON format:
        {{
            "skills": [
                {{
                    "name_ar": "اسم المهارة",
                    "description_ar": "وصف تفصيلي للمهارة",
                    "difficulty": 1,
                    "key_concepts": ["مفهوم ١", "مفهوم ٢"]
                }}
            ]
        }}

        Dialogue to analyze:
        {json.dumps(dialogue_content, ensure_ascii=False)}
        """
        return skill_extraction_prompt
    
    def generate_questions_for_skill(self, skill: Dict) -> str:
        """
        Generate a prompt to create questions for a specific skill.
        This would be used with your preferred LLM.
        """
        question_prompt = f"""
        Create multiple-choice and true/false questions in Arabic to test this skill:
        
        Skill Name: {skill['name_ar']}
        Description: {skill['description_ar']}
        Difficulty Level: {skill['difficulty']}
        
        Generate 3 questions for this skill following these requirements:
        1. Questions must be in Arabic
        2. Include a mix of multiple-choice and true/false
        3. Provide specific feedback for correct/incorrect answers
        4. Include shape meta tags where needed
        5. All questions should be at the same difficulty level
        
        Output format:
        {{
            "questions": [
                {{
                    "text_ar": "نص السؤال",
                    "type": "multiple_choice",
                    "choices": ["خيار ١", "خيار ٢", "خيار ٣", "خيار ٤"],
                    "correct_answer": "الإجابة الصحيحة",
                    "feedback_correct_ar": "تعليق إيجابي",
                    "feedback_incorrect_ar": "شرح الخطأ",
                    "shape_meta": "<shape type=\"نوع الشكل\" .../>",
                    "difficulty": 1
                }}
            ]
        }}
        """
        return question_prompt

    def process_llm_response(self, llm_response: str) -> Tuple[bool, Dict]:
        """Process and validate LLM-generated content"""
        try:
            content = json.loads(llm_response)
            
            # Validate terminology
            errors = []
            for exchange in content.get('dialogue_ar', {}).get('exchanges', []):
                for key in ['teacher', 'student']:
                    if key in exchange:
                        valid_terms, term_errors = self.terminology_validator.check_terminology_usage(exchange[key])
                        if not valid_terms:
                            errors.extend(term_errors)
            
            if errors:
                return False, {'errors': errors}
            
            return True, content
            
        except json.JSONDecodeError as e:
            return False, {'errors': [f"Invalid JSON format: {str(e)}"]}
        except Exception as e:
            return False, {'errors': [f"Error processing content: {str(e)}"]}

    def save_lesson_content(self, content: Dict, output_path: str):
        """Save processed lesson content to file"""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(content, f, ensure_ascii=False, indent=2)

def main():
    """Example usage of the DialogueSkillGenerator"""
    generator = DialogueSkillGenerator()
    
    # Example topic
    topic = "multiplication"
    grade = 3
    unit = 1
    
    # 1. Generate dialogue prompt
    dialogue_prompt = generator.generate_lesson_dialogue(topic, grade, unit)
    print("\nGenerated Dialogue Prompt:")
    print(dialogue_prompt)
    
    # In practice, you would send this prompt to your LLM and get a response
    # For this example, we'll use sample content
    sample_dialogue = {
        "title_ar": "درس الضرب",
        "grade": 3,
        "unit": 1,
        "dialogue_ar": {
            "exchanges": [
                {
                    "teacher": "اليوم سنتعلم عن الضرب",
                    "student": "ما هو الضرب؟"
                }
            ]
        }
    }
    
    # 2. Extract skills prompt
    skills_prompt = generator.extract_skills_from_dialogue(sample_dialogue)
    print("\nGenerated Skills Extraction Prompt:")
    print(skills_prompt)
    
    # 3. Generate questions for a sample skill
    sample_skill = {
        "name_ar": "فهم مفهوم الضرب",
        "description_ar": "القدرة على فهم الضرب كعملية تكرار الجمع",
        "difficulty": 1
    }
    
    questions_prompt = generator.generate_questions_for_skill(sample_skill)
    print("\nGenerated Questions Prompt:")
    print(questions_prompt)

if __name__ == "__main__":
    main()
