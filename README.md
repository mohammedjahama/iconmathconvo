# Math Lesson Generator System

This system helps generate and validate Arabic math lessons using Large Language Models (LLMs). It provides structured prompts for lesson generation and tools for validating and processing the generated content.

## Generated Content

The repository includes pre-generated content:
- Grade 3 lessons split into multiple parts (`split_lessons/lessons_grade3_part1.csv`, `split_lessons/lessons_grade3_part2.csv`)
- Grade 3 questions in various segments (`split_questions/questions_grade3_part111.csv`, `split_questions/questions_grade3_part1223moresplits.csv`, `split_questions/questions_grade3_part2.csv`)
- Generated math dialogues in both English and Arabic (`math_dialogues.txt`, `math_dialogues_arabic.txt`)
- Bilingual math terminology reference (`math_terminology_bilingual.txt`)
- Math glossary and dialogue templates (`math_glossary.txt`, `dialogue_templates.txt`)

## System Components

1. `llm_prompts.txt` - Contains prompt templates for generating:
   - Lesson dialogues in Arabic
   - Skills and learning objectives
   - Multiple choice/true-false questions
   - Shape descriptions with meta tags
   - Feedback for correct/incorrect answers

2. `lesson_generator.py` - Core classes for lesson structure:
   - `Lesson`: Manages lesson content and exam generation
   - `Skill`: Represents specific skills taught in lessons
   - `Question`: Handles question content and grading

3. `validate_llm_output.py` - Validates LLM-generated content:
   - JSON structure validation
   - Arabic text verification
   - Shape meta tag validation
   - Question format checking

4. `sample_lesson_data.json` - Example lesson structure

5. `dialogue_skill_generator.py` - Generates dialogues and skills:
   - Creates natural teacher-student conversations
   - Extracts skills from dialogues
   - Generates skill-based questions
   - Validates terminology

6. `exam_generator.py` - Handles exam creation and grading:
   - Creates balanced assessments
   - Manages question banks
   - Provides skill-based feedback
   - Generates recommendations

7. `main.py` - Orchestrates the complete workflow:
   - Coordinates all components
   - Manages file operations
   - Handles LLM integration
   - Processes results

## Workflow

1. **Generate Lesson Content**
   - Use the prompts from `llm_prompts.txt` with your preferred LLM
   - The prompts ensure consistent JSON structure and Arabic content
   - Include shape meta tags for geometric content

2. **Validate Generated Content**
   ```python
   from validate_llm_output import process_llm_output
   
   # Process LLM output
   success, result = process_llm_output(llm_generated_json)
   if success:
       print("Content validation passed")
   else:
       print("Validation errors:", result)
   ```

3. **Create Lesson Object**
   ```python
   from lesson_generator import Lesson, Skill, Question
   
   # Create lesson from validated JSON
   lesson = Lesson(
       title_ar=content['title_ar'],
       grade=content['grade'],
       unit=content['unit']
   )
   ```

## Shape Meta Tags

Use these tags to describe geometric shapes in questions:

```
Square:    <shape type="square" width="5cm"/>
Rectangle: <shape type="rectangle" width="6cm" height="4cm"/>
Triangle:  <shape type="triangle" base="4cm" height="3cm"/>
Circle:    <shape type="circle" radius="3cm"/>
```

## Example LLM Prompt Usage

1. Choose a topic and grade level
2. Copy the appropriate prompt from `llm_prompts.txt`
3. Replace placeholders with your specific requirements
4. Send to your LLM
5. Validate the generated content
6. Use the content in your lesson system

Example:
```
Please generate a complete math lesson in Arabic about {TOPIC} for grade {GRADE}, unit {UNIT}.
The lesson should help students understand:
- {LEARNING_OBJECTIVE_1}
- {LEARNING_OBJECTIVE_2}
- {LEARNING_OBJECTIVE_3}

Follow the OUTPUT FORMAT structure exactly and ensure all content is in Arabic.
```

## Content Requirements

1. **Dialogue**
   - Natural conversation between teacher and student
   - Clear concept introduction and explanation
   - Student questions showing curiosity and understanding

2. **Skills**
   - Clear, measurable learning objectives
   - Relevant to grade level
   - Progressive skill development

3. **Questions**
   - Multiple choice or true/false format
   - Clear distractors
   - Constructive feedback
   - Shape descriptions where needed

4. **Arabic Content**
   - Proper grammar and terminology
   - Grade-appropriate language
   - Clear mathematical explanations

## Validation Checks

The system validates:
- JSON structure
- Arabic text presence
- Required fields
- Question format
- Shape meta tags
- Feedback presence
- Choice/answer consistency

## Best Practices

1. **Content Generation**
   - Use grade-appropriate examples
   - Include real-world applications
   - Ensure progressive difficulty
   - Maintain consistent terminology

2. **Questions**
   - Test different aspects of understanding
   - Include visual elements where helpful
   - Provide specific, constructive feedback
   - Ensure automatic grading capability

3. **Shapes**
   - Use appropriate dimensions
   - Include clear meta descriptions
   - Consider Arabic text direction
   - Maintain consistent units (cm)

4. **Validation**
   - Always validate LLM output
   - Check Arabic text quality
   - Verify mathematical accuracy
   - Test question/answer consistency

## LLM Integration Guide

### Recommended Model: GPT-4

GPT-4 is recommended for this system because:
- Excellent Arabic language capabilities
- Strong understanding of mathematical concepts
- Reliable structured output in JSON
- Consistent terminology usage
- High-quality dialogue generation

Alternative models:
- Claude-2: Good alternative, especially for complex reasoning
- GPT-3.5-Turbo: Budget option, may need more validation

### API Setup

1. Create a `.env` file:
```
OPENAI_API_KEY=your_key_here
```

2. Add to main.py:
```python
import os
from dotenv import load_dotenv
import openai

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# In MathLessonSystem class:
async def generate_with_llm(self, prompt: str) -> str:
    response = await openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert math educator specializing in Arabic mathematics education."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content
```

### Cost Estimates (per lesson)
- Dialogue generation: ~800 tokens
- Skill extraction: ~500 tokens
- Questions (3 per skill): ~1000 tokens
- Total: ~2300 tokens
- Approximate cost with GPT-4: $0.07

### Directory Structure
```
project_root/
├── generated_lessons/
├── generated_exams/
└── student_results/
```

The system is ready to use after setting up your API key and installing required packages:
```bash
pip install openai python-dotenv
