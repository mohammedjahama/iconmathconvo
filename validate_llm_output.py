import json
import re
from typing import Dict, List, Union, Tuple, Set

class TerminologyValidator:
    """Validates the use of standardized Arabic mathematical terminology"""
    
    def __init__(self):
        # Standard terminology mappings (English to Arabic)
        self.terminology = {
            # Numbers and Operations
            "multiplication": "الضرب",
            "division": "القسمة",
            "factor": "العامل",
            "product": "ناتج الضرب",
            "dividend": "المقسوم",
            "divisor": "المقسوم عليه",
            "quotient": "ناتج القسمة",
            "equal groups": "مجموعات متساوية",
            "multiple": "مضاعف",
            
            # Arrays and Groups
            "array": "مصفوفة",
            "row": "صف",
            "column": "عمود",
            "equal parts": "أجزاء متساوية",
            "group": "مجموعة",
            "pattern": "نمط",
            
            # Problem-Solving Terms
            "equal sharing": "التوزيع المتساوي",
            "equal grouping": "التجميع المتساوي",
            "unknown factor": "العامل المجهول",
            "missing number": "العدد المفقود",
            "word problem": "مسألة كلامية",
            
            # Properties
            "commutative property": "خاصية التبديل",
            "associative property": "خاصية التجميع",
            "distributive property": "خاصية التوزيع",
            
            # Visual Models
            "number line": "خط الأعداد",
            "area model": "نموذج المساحة",
            "grid": "شبكة",
            "rectangle model": "نموذج المستطيل",
            
            # Instruction Terms
            "solve": "حل",
            "calculate": "احسب",
            "explain": "اشرح",
            "show your work": "اعرض خطوات الحل",
            "check your answer": "تحقق من إجابتك",
            "draw": "ارسم",
            
            # Comparison Terms
            "greater than": "أكبر من",
            "less than": "أصغر من",
            "equal to": "يساوي",
            "more": "أكثر",
            "fewer": "أقل"
        }
        
        # Create set of Arabic terms for quick lookup
        self.arabic_terms = set(self.terminology.values())
    
    def check_terminology_usage(self, text: str) -> Tuple[bool, List[str]]:
        """Check if the text uses proper Arabic mathematical terminology"""
        errors = []
        found_terms = set()
        
        # Check for each Arabic term in the text
        for term in self.arabic_terms:
            if term in text:
                found_terms.add(term)
        
        # Look for potential terminology errors (common mistakes or variations)
        # This could be expanded based on common error patterns
        common_errors = {
            r"ضرب": "الضرب",  # Missing 'ال'
            r"قسمة": "القسمة",
            r"عامل": "العامل",
            r"مقسوم": "المقسوم"
        }
        
        for error_pattern, correct_term in common_errors.items():
            if re.search(rf"\b{error_pattern}\b", text) and correct_term not in found_terms:
                errors.append(f"Found '{error_pattern}' - should use '{correct_term}'")
        
        return len(errors) == 0, errors

def validate_arabic_text(text: str) -> bool:
    """Check if text contains Arabic characters"""
    arabic_pattern = re.compile(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF]+')
    return bool(arabic_pattern.search(text))

def validate_shape_meta(shape_meta: str) -> Tuple[bool, str]:
    """Validate shape meta tag format"""
    if not shape_meta:
        return True, ""
    
    valid_shapes = ["square", "rectangle", "triangle", "circle"]
    required_attributes = {
        "square": ["width"],
        "rectangle": ["width", "height"],
        "triangle": ["base", "height"],
        "circle": ["radius"]
    }
    
    shape_pattern = r'<shape\s+type="([^"]+)"([^>]+)/>'
    match = re.match(shape_pattern, shape_meta)
    if not match:
        return False, "Invalid shape meta tag format"
    
    shape_type = match.group(1)
    attributes = match.group(2)
    
    if shape_type not in valid_shapes:
        return False, f"Invalid shape type. Must be one of: {', '.join(valid_shapes)}"
    
    required = required_attributes[shape_type]
    for attr in required:
        if f'{attr}="' not in attributes:
            return False, f"Missing required attribute '{attr}' for shape type '{shape_type}'"
    
    return True, ""

def validate_lesson_content(content: Dict) -> List[str]:
    """Validate the LLM-generated lesson content"""
    errors = []
    terminology_validator = TerminologyValidator()
    
    # Required top-level fields
    required_fields = ["title_ar", "grade", "unit", "dialogue_ar", "skills"]
    for field in required_fields:
        if field not in content:
            errors.append(f"Missing required field: {field}")
    
    # Validate Arabic title and terminology
    if "title_ar" in content:
        if not validate_arabic_text(content["title_ar"]):
            errors.append("Title must contain Arabic text")
        valid_terms, term_errors = terminology_validator.check_terminology_usage(content["title_ar"])
        errors.extend(term_errors)
    
    # Validate dialogue structure and terminology
    if "dialogue_ar" in content:
        if not isinstance(content["dialogue_ar"], dict) or "exchanges" not in content["dialogue_ar"]:
            errors.append("dialogue_ar must contain 'exchanges' array")
        else:
            for i, exchange in enumerate(content["dialogue_ar"]["exchanges"]):
                if not any(key in exchange for key in ["teacher", "student"]):
                    errors.append(f"Exchange {i} must contain either 'teacher' or 'student' key")
                for key in ["teacher", "student"]:
                    if key in exchange:
                        text = exchange[key]
                        if not validate_arabic_text(text):
                            errors.append(f"Exchange {i} {key} must contain Arabic text")
                        valid_terms, term_errors = terminology_validator.check_terminology_usage(text)
                        errors.extend([f"Exchange {i} {key}: {err}" for err in term_errors])
    
    # Validate skills and terminology
    if "skills" in content:
        if not isinstance(content["skills"], list):
            errors.append("skills must be an array")
        else:
            for i, skill in enumerate(content["skills"]):
                if "name_ar" not in skill:
                    errors.append(f"Skill {i} missing name_ar")
                if "description_ar" not in skill:
                    errors.append(f"Skill {i} missing description_ar")
                if "questions" not in skill:
                    errors.append(f"Skill {i} missing questions")
                
                # Validate skill terminology
                for field in ["name_ar", "description_ar"]:
                    if field in skill:
                        valid_terms, term_errors = terminology_validator.check_terminology_usage(skill[field])
                        errors.extend([f"Skill {i} {field}: {err}" for err in term_errors])
                
                # Validate questions
                if "questions" in skill:
                    for j, question in enumerate(skill["questions"]):
                        required_q_fields = ["text_ar", "correct_answer", "choices", 
                                          "feedback_correct_ar", "feedback_incorrect_ar"]
                        for field in required_q_fields:
                            if field not in question:
                                errors.append(f"Question {j} in skill {i} missing {field}")
                        
                        # Validate question terminology
                        for field in ["text_ar", "feedback_correct_ar", "feedback_incorrect_ar"]:
                            if field in question:
                                valid_terms, term_errors = terminology_validator.check_terminology_usage(question[field])
                                errors.extend([f"Question {j} in skill {i} {field}: {err}" for err in term_errors])
                        
                        # Validate choices
                        if "choices" in question and "correct_answer" in question:
                            if question["correct_answer"] not in question["choices"]:
                                errors.append(f"Question {j} in skill {i}: correct_answer must be one of the choices")
                        
                        # Validate shape meta if present
                        if "shape_meta" in question:
                            is_valid, error_msg = validate_shape_meta(question["shape_meta"])
                            if not is_valid:
                                errors.append(f"Question {j} in skill {i}: {error_msg}")
    
    return errors

def format_validation_report(errors: List[str]) -> str:
    """Format validation errors into a readable report"""
    if not errors:
        return "✓ Content validation passed. No errors found."
    
    report = "Content Validation Report:\n"
    report += "========================\n"
    report += f"Found {len(errors)} error(s):\n\n"
    
    for i, error in enumerate(errors, 1):
        report += f"{i}. {error}\n"
    
    return report

def process_llm_output(json_str: str) -> Tuple[bool, Union[Dict, str]]:
    """Process and validate LLM-generated content"""
    try:
        # Parse JSON
        content = json.loads(json_str)
        
        # Validate content
        errors = validate_lesson_content(content)
        
        if errors:
            return False, format_validation_report(errors)
        
        return True, content
        
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON format: {str(e)}"
    except Exception as e:
        return False, f"Error processing content: {str(e)}"

if __name__ == "__main__":
    # Example usage
    with open('sample_lesson_data.json', 'r', encoding='utf-8') as f:
        json_str = f.read()
    
    success, result = process_llm_output(json_str)
    if success:
        print("✓ Content validation passed")
        print("\nProcessed content:")
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(result)  # Print validation errors
