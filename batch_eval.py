import pandas as pd
from sentiment_llm import process_csv_file
import argparse

def main():
    parser = argparse.ArgumentParser(description='Batch process movie reviews')
    parser.add_argument('--input', '-i', required=True, help='Input CSV file path')
    parser.add_argument('--output', '-o', required=True, help='Output CSV file path')
    
    args = parser.parse_args()
    
    print(f"Processing {args.input}...")
    process_csv_file(args.input, args.output)
    print("Batch processing completed!")

if __name__ == "__main__":
    main()