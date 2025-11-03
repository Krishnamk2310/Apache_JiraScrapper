# Apache JIRA Scraper  
**Author:** Markandey Krishna Mishra
**Enrollment Number:** E22CSEU0671  
**Institution:** Bennett University  

---

## 📘 Overview  
The **Apache JIRA Scraper** is a Python-based project built to collect, clean, and transform issue data from **Apache’s public JIRA instance**.  
The goal is to prepare structured, high-quality datasets suitable for machine learning, analytics, or LLM (Large Language Model) training.  

This scraper is designed to be **fault-tolerant**, **resumable**, and **easy to extend**, making it a reliable base for large-scale data collection pipelines.

---

## 🚀 Features  

- **Automatic Pagination:** Fetches all available issues for selected projects.  
- **Retry & Rate-Limiting:** Handles failed requests and rate limits gracefully.  
- **Resumable Scraping:** Automatically resumes from the last processed issue.  
- **Data Transformation:** Cleans and structures issue data into JSONL format.  
- **Raw Data Backup:** Stores all raw JSONs for reproducibility and debugging.  
- **Fault Tolerance:** Retries on common HTTP and network failures.  
- **Ready for LLMs:** Generates well-structured text data for training datasets.  

---

## Setup

1. Make sure you have Python installed

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run with default projects (TIKA, ZOOKEEPER, OPENNLP):

```bash
python main.py
```

Run with specific projects:

```bash
python main.py --projects HADOOP SPARK KAFKA
```

Transform existing data without scraping:

```bash
python main.py --transform-only
```

## Output

The script creates two types of output:

1. Raw data: `data/raw/<PROJECT>/<ISSUE>.json`
   - Contains complete JSON data for each issue
   - Organized by project folders

2. Processed data: `data/train.jsonl`
   - One JSON object per line
   - Contains cleaned and transformed issue data
   - Includes: key, summary, description, status, comments
   - Example of a cleaned JSON line (one per line in `data/train.jsonl`)

```json
{
  "key": "ZOOKEEPER-4523",
  "summary": "Improve leader election performance under heavy load",
  "description": "Optimized the leader election algorithm by reducing redundant message exchanges and implementing better timeout handling for edge cases.",
  "status": "Closed",
  "created": "2023-06-15T09:20:00.000+0000",
  "comments": [
    {
      "author": "John Doe",
      "text": "This update significantly improved performance on our test clusters. Great work!",
      "created": "2023-06-17T11:45:00.000+0000"
    },
    {
      "author": "Jane Smith",
      "text": "Confirmed fix works as expected in version 3.9.0.",
      "created": "2023-06-18T15:12:00.000+0000"
    }
  ]
}

```

## Project Structure

- `main.py` - Main script to run
- `jira_scraper.py` - Handles JIRA API interaction
- `text_utils.py` - Text cleaning and transformation

- `config.py` - Configuration and constants

## Design and reasoning

I kept the code simple and readable. Each file has one job.

- Single-threaded scraping keeps behavior predictable and avoids aggressive load on the public API.
- Retry + small sleeps make the scraper more polite and reduce failures.
- Saving raw JSON helps debugging and lets you re-run transformations without re-downloading.

## Edge cases handled

- Paging: fetches pages until no more issues are left.
- 429/Rate-limit safety: retries and pauses between pages reduce chance of being throttled.
- Network errors: transient failures are retried by the HTTP session configuration.
- Missing data: transformer uses defaults so missing fields won't crash the run.
- Clean text output: HTML tags stripped and HTML entities decoded for readable text.
- Partial runs: processed issue keys are saved so a stopped run can resume.
