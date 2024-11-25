import csv
import math

def split_csv(input_file, output_prefix, total_rows, num_files):
    chunk_size = math.ceil(total_rows / num_files)
    
    with open(input_file, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)  # Read the header row
        
        chunk = []
        chunk_num = 1
        
        for row in reader:
            chunk.append(row)
            
            if len(chunk) >= chunk_size and chunk_num < num_files:
                write_chunk(chunk, header, output_prefix, chunk_num)
                chunk = []
                chunk_num += 1
        
        # Write the last chunk (which may have more rows than the others)
        if chunk:
            write_chunk(chunk, header, output_prefix, chunk_num)

def write_chunk(chunk, header, output_prefix, chunk_num):
    output_file = f"{output_prefix}_part{chunk_num}.csv"
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        writer.writerows(chunk)
    print(f"Wrote {len(chunk)} rows to {output_file}")

# Split lessons_grade3, full list, not full questions associated.csv
split_csv('lessons_grade3, full list, not full questions associated.csv', 'lessons_grade3', 130, 5)

# Split updated_questions_grade3.csv
split_csv('updated_questions_grade3.csv', 'questions_grade3', 255, 5)

print("CSV splitting complete.")