# Wikidata-CSV-file-annotation-tool
Wikidata CSV file annotation tool

## Description
A Python script that automatically matches cell values from CSV files to corresponding Wikidata entities using the Wikidata API, generating a new CSV with matched entities.

## Features
- Processes each cell in CSV files to find matching Wikidata entities
- Outputs clean results with only successful matches
- Formats Wikidata QIDs as complete URLs (e.g., http://www.wikidata.org/entity/Q42)
- Includes rate limiting to comply with Wikidata API policies
- Command-line interface for easy integration into workflows

## Installation
1. Python 3.6+ required
2. Install dependencies:
pip install requests


## Usage
Basic command:
python wikidata_matcher.py input.csv output.csv


Advanced options:
python wikidata_matcher.py input.csv output.csv --file_id custom_id


### Arguments
- `input.csv`: Path to your input CSV file (required)
- `output.csv`: Path for the results CSV file (required)
- `--file_id`: Optional identifier for the file (defaults to input filename)

## Output Format
The results CSV contains these columns:
1. `file_id` - Source file identifier
2. `row_id` - Row number (1-based index)
3. `col_id` - Column number (1-based index)
4. `wikidata_qid` - Full Wikidata entity URL
5. `wikidata_label` - Official label from Wikidata

## Example

### Input (sample.csv):
City,Country
Paris,France
Tokyo,Japan


### Command:
python wikidata_matcher.py sample.csv results.csv


### Output (results.csv):
file_id,row_id,col_id,wikidata_qid,wikidata_label
sample,1,1,http://www.wikidata.org/entity/Q90,Paris
sample,1,2,http://www.wikidata.org/entity/Q142,France
sample,2,1,http://www.wikidata.org/entity/Q1490,Tokyo
sample,2,2,http://www.wikidata.org/entity/Q17,Japan


## API Etiquette
The script includes a 0.5 second delay between requests. For large datasets:
- Run during off-peak hours (UTC 00:00-06:00)
- Consider local caching of results
- Contact Wikimedia for bulk access if needed

## Support
Please open an issue on GitHub for:
- Bug reports
- Feature requests
- Usage questions

## License
MIT License