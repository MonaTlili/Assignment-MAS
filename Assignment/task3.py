"""
    1. Use the textfile named “pg2701”
    2. Split the text file to chunks (group of sentences)
    3. Clean the data and count the words using single and multi-thread
    4. Identify processing times between them
    5. Explain the difference in performance
"""

import time
import requests
from multiprocessing import Pool, cpu_count

# file_path = r'https://raw.githubusercontent.com/MonaTlili/Assignment-MAS/refs/heads/main/Moby_dick/pg2701.txt'
# with open(file_path, "r", encoding="utf-8") as file:
#     sample_text = file.read()

file_path = 'https://raw.githubusercontent.com/MonaTlili/Assignment-MAS/refs/heads/main/Moby_dick/pg2701.txt'
response = requests.get(file_path, timeout=10) # Timeout is counted in seconds
sample_text = response.text

# Splitting the text into sentences for smaller chunks of data
text_cleaned = sample_text.replace('!', '.').replace('?', '.')
text_chunks = text_cleaned.split('.')

# Map function to process a chunk of text
def map_function(chunk):
    word_counts = {}
    words = chunk.split()

    for word in words:
        word = word.lower().strip(""" ,.()!?*'“”’}{ """)  # Cleaning the word
        if word:
            word_counts[word] = word_counts.get(word, 0) + 1

    return word_counts

# Function to combine results (shuffle and reduce)
def combine_results(results):
    combined_counts = {}

    for result in results:
        for word, count in result.items():
            combined_counts[word] = combined_counts.get(word, 0) + count

    return combined_counts

# Parallel MapReduce implementation
def parallel_mapreduce(text_chunks):
    # Create a multiprocessing pool with the number of available CPU cores
    with Pool(cpu_count()) as pool:
        # Step 1: Map phase - distribute chunks to multiple processes
        map_results = pool.map(map_function, text_chunks)

        # Step 2: Shuffle and Reduce phase - aggregate results
        final_word_counts = combine_results(map_results)

    return final_word_counts

# Single-threaded version of word count
def single_threaded_word_count(text):
    word_counts = {}
    words = text.split()

    for word in words:
        word = word.lower().strip(""" ,.()!?*'“”’}{ """)
        if word:
            word_counts[word] = word_counts.get(word, 0) + 1

    return word_counts

# Performance testing
if __name__ == "__main__":
    # Test data
    text = sample_text
    chunks = text_chunks

    print("Starting performance comparison...\n")

    # Single-threaded execution 
    # start_time = time.time()
    # single_threaded_counts = single_threaded_word_count(text)
    # single_threaded_duration = time.time() - start_time
    
    start_time = time.perf_counter()
    single_threaded_counts = single_threaded_word_count(text)
    single_threaded_duration = time.perf_counter() - start_time

    print("Single-threaded Word Count:")
    print(single_threaded_counts)
    print(f"Single-threaded Duration: {single_threaded_duration:.6f} seconds\n")

    # Multi-threaded (MapReduce) execution
    # start_time = time.time()
    # parallel_counts = parallel_mapreduce(chunks)
    # parallel_duration = time.time() - start_time
    
    start_time = time.perf_counter()
    parallel_counts = parallel_mapreduce(chunks)
    parallel_duration = time.perf_counter() - start_time

    print("Parallel (MapReduce) Word Count:")
    print(parallel_counts)
    print(f"Parallel Duration: {parallel_duration:.6f} seconds\n")

    # Performance Summary
    print("Performance Comparison:")
    print(f"Single-threaded Time: {single_threaded_duration:.6f} seconds")
    print(f"Parallel Time: {parallel_duration:.6f} seconds")
    print(f"Speedup: {single_threaded_duration / parallel_duration:.2f}x (depending on dataset size)")
