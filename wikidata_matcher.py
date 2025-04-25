import csv
import requests
import argparse
import time
from urllib.parse import quote

def search_wikidata(search_term):
    """Search Wikidata and return top Q-ID and label."""
    params = {
        "action": "query",
        "list": "search",
        "srsearch": search_term,
        "format": "json",
        "srlimit": 1  # Get only the top result
    }
    try:
        response = requests.get("https://www.wikidata.org/w/api.php", params=params)
        response.raise_for_status()
        data = response.json()
        if "search" in data.get("query", {}) and data["query"]["search"]:
            result = data["query"]["search"][0]
            qid = result.get("title", "")
            if qid.startswith("Q"):
                return {
                    "qid": f"http://www.wikidata.org/entity/{qid}",
                    "label": result.get("snippet", "").replace('<span class="searchmatch">', '').replace('</span>', '')
                }
    except Exception as e:
        print(f"Error searching for '{search_term}': {e}")
    return None

def process_csv(input_file, output_file, file_id):
    """Process CSV file and write results."""
    with open(input_file, mode='r', encoding='utf-8') as infile, \
         open(output_file, mode='w', encoding='utf-8', newline='') as outfile:
        
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        
        # Write header
        writer.writerow(["tab_id", "row_id", "col_id", "entity", "wikidata_label"])
        
        for row_idx, row in enumerate(reader, start=0):
            for col_idx, cell_value in enumerate(row, start=0):
                if cell_value.strip():  # Skip empty cells
                    print(f"Processing: Row {row_idx}, Col {col_idx} -> '{cell_value}'")
                    result = search_wikidata(cell_value)
                    if result:  # Only write if we found a match
                        writer.writerow([
                            file_id,
                            row_idx,
                            col_idx,
                            result["qid"],
                            result["label"]
                        ])
                    time.sleep(0.5)  # Be kind to the API

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Search Wikidata for CSV cell values.')
    parser.add_argument('input_file', help='Input CSV file path')
    parser.add_argument('output_file', help='Output CSV file path')
    parser.add_argument('--file_id', default='', help='Optional file identifier')
    
    args = parser.parse_args()
    
    # Use filename as file_id if not provided
    file_id = args.file_id if args.file_id else os.path.splitext(os.path.basename(args.input_file))[0]
    
    print(f"Processing {args.input_file} -> {args.output_file} (file_id: {file_id})")
    process_csv(args.input_file, args.output_file, file_id)
    print(f"Done! Results saved to {args.output_file}")