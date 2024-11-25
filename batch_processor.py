import asyncio
import json
import os
import time
from datetime import datetime
from typing import List, Dict
import aiohttp
from dotenv import load_dotenv
from dialogue_skill_generator import DialogueSkillGenerator
from exam_generator import ExamGenerator
from validate_llm_output import process_llm_output

class BatchProcessor:
    def __init__(self, batch_size: int = 5):
        load_dotenv()
        self.batch_size = batch_size
        self.dialogue_generator = DialogueSkillGenerator()
        self.exam_generator = ExamGenerator()
        
        # Create output directories
        os.makedirs('generated_lessons', exist_ok=True)
        os.makedirs('generated_exams', exist_ok=True)
        os.makedirs('logs', exist_ok=True)
        
        # Initialize progress tracking
        self.progress = {
            'total_lessons': 0,
            'completed_lessons': 0,
            'failed_lessons': 0,
            'start_time': None,
            'end_time': None,
            'token_usage': 0,
            'errors': []
        }
        
        # Rate limiting
        self.request_times = []
        self.rate_limit = 50  # requests per minute
        
    async def process_lesson(self, topic: str, grade: int, unit: int) -> Dict:
        """Process a single lesson with error handling and retries"""
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                # Implement rate limiting
                await self.check_rate_limit()
                
                # Generate dialogue
                dialogue_prompt = self.dialogue_generator.generate_lesson_dialogue(
                    topic=topic,
                    grade=grade,
                    unit=unit
                )
                dialogue_content = await self.call_llm(dialogue_prompt)
                
                # Validate dialogue
                success, result = process_llm_output(dialogue_content)
                if not success:
                    raise ValueError(f"Dialogue validation failed: {result}")
                
                # Extract skills
                skills_prompt = self.dialogue_generator.extract_skills_from_dialogue(result)
                skills_content = await self.call_llm(skills_prompt)
                
                # Generate questions for each skill
                for skill in skills_content['skills']:
                    questions_prompt = self.dialogue_generator.generate_questions_for_skill(skill)
                    questions = await self.call_llm(questions_prompt)
                    skill['questions'] = questions['questions']
                
                # Create and save lesson content
                lesson_content = {
                    **result,
                    'skills': skills_content['skills']
                }
                
                return lesson_content
                
            except Exception as e:
                retry_count += 1
                if retry_count == max_retries:
                    self.log_error(f"Failed to process lesson {topic}: {str(e)}")
                    raise
                await asyncio.sleep(2 ** retry_count)  # Exponential backoff
    
    async def process_batch(self, lessons: List[Dict]) -> None:
        """Process a batch of lessons concurrently"""
        tasks = []
        for lesson in lessons:
            task = asyncio.create_task(
                self.process_lesson(
                    topic=lesson['topic'],
                    grade=lesson['grade'],
                    unit=lesson['unit']
                )
            )
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                self.progress['failed_lessons'] += 1
                self.log_error(f"Lesson {lessons[i]['topic']} failed: {str(result)}")
            else:
                self.progress['completed_lessons'] += 1
                self.save_lesson(result, lessons[i]['topic'])
    
    async def process_all_lessons(self, lessons: List[Dict]) -> None:
        """Process all lessons in batches"""
        self.progress['total_lessons'] = len(lessons)
        self.progress['start_time'] = datetime.now()
        
        # Process in batches
        for i in range(0, len(lessons), self.batch_size):
            batch = lessons[i:i + self.batch_size]
            await self.process_batch(batch)
            
            # Save progress after each batch
            self.save_progress()
            
            # Brief pause between batches
            await asyncio.sleep(1)
        
        self.progress['end_time'] = datetime.now()
        self.save_progress()
        self.generate_report()
    
    async def check_rate_limit(self) -> None:
        """Implement rate limiting"""
        now = time.time()
        minute_ago = now - 60
        
        # Remove old requests
        self.request_times = [t for t in self.request_times if t > minute_ago]
        
        # If at rate limit, wait
        if len(self.request_times) >= self.rate_limit:
            wait_time = self.request_times[0] - minute_ago
            await asyncio.sleep(wait_time)
        
        self.request_times.append(now)
    
    async def call_llm(self, prompt: str) -> Dict:
        """Make API call to LLM with rate limiting"""
        # Here you would implement your actual LLM API call
        # For now, returning sample data
        return {"sample": "data"}
    
    def save_lesson(self, content: Dict, topic: str) -> None:
        """Save processed lesson content"""
        filename = f"generated_lessons/lesson_{content['grade']}_{topic.replace(' ', '_')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(content, f, ensure_ascii=False, indent=2)
    
    def save_progress(self) -> None:
        """Save progress to file"""
        progress_file = 'logs/progress.json'
        with open(progress_file, 'w', encoding='utf-8') as f:
            json.dump(self.progress, f, ensure_ascii=False, indent=2)
    
    def log_error(self, error: str) -> None:
        """Log error with timestamp"""
        timestamp = datetime.now().isoformat()
        self.progress['errors'].append({
            'timestamp': timestamp,
            'error': error
        })
        
        # Also write to error log file
        with open('logs/errors.log', 'a', encoding='utf-8') as f:
            f.write(f"[{timestamp}] {error}\n")
    
    def generate_report(self) -> None:
        """Generate final processing report"""
        duration = self.progress['end_time'] - self.progress['start_time']
        
        report = {
            'total_lessons': self.progress['total_lessons'],
            'completed_lessons': self.progress['completed_lessons'],
            'failed_lessons': self.progress['failed_lessons'],
            'duration_seconds': duration.total_seconds(),
            'token_usage': self.progress['token_usage'],
            'error_count': len(self.progress['errors']),
            'start_time': self.progress['start_time'].isoformat(),
            'end_time': self.progress['end_time'].isoformat()
        }
        
        with open('logs/final_report.json', 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

async def main():
    # Example usage
    processor = BatchProcessor(batch_size=5)
    
    # Sample lessons to process
    lessons = [
        {'topic': 'multiplication', 'grade': 3, 'unit': 1},
        {'topic': 'division', 'grade': 3, 'unit': 2},
        # Add more lessons...
    ]
    
    await processor.process_all_lessons(lessons)

if __name__ == "__main__":
    asyncio.run(main())
