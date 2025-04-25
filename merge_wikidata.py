import csv
import glob
import os
import argparse

def merge_wikidata_csvs(input_pattern, output_file):
    """
    Merge multiple Wikidata CSV files into one consolidated file.
    
    Args:
        input_pattern (str): Glob pattern to match input files (e.g., 'results/*.csv')
        output_file (str): Path for the merged output CSV
    """
    # Get all matching files
    input_files = glob.glob(input_pattern)
    
    if not input_files:
        print(f"No files found matching pattern: {input_pattern}")
        return
    
    print(f"Merging {len(input_files)} files into {output_file}")
    
    # Initialize variables
    header_written = False
    merged_count = 0
    
    with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        
        for filepath in input_files:
            with open(filepath, 'r', encoding='utf-8') as infile:
                reader = csv.reader(infile)
                header = next(reader)  # Read header
                
                # Write header only once
                if not header_written:
                    writer.writerow(header)
                    header_written = True
                
                # Write all rows
                for row in reader:
                    writer.writerow(row)
                    merged_count += 1
                
            print(f"Processed {os.path.basename(filepath)}: {merged_count} total rows")
    
    print(f"Merge complete! Total rows: {merged_count}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Merge multiple Wikidata CSV files into one.')
    parser.add_argument('input_pattern', help='Glob pattern for input files (e.g., "results/*.csv")')
    parser.add_argument('output_file', help='Path for the merged output CSV file')
    
    args = parser.parse_args()
    
    merge_wikidata_csvs(args.input_pattern, args.output_file)