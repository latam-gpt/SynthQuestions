import time
import re
import requests
from typing import List, Dict, Optional
from ddgs import DDGS
from rank_bm25 import BM25Okapi
from bs4 import BeautifulSoup


def web_search_by_keywords(keywords: List[str], backend: str="duckduckgo") -> Optional[Dict]:
    """
    Takes a list of keywords and returns the single most relevant document using BM25 scoring.

    Args:
        keywords: List of keywords for the search query
        backend: Search backend to use

    Returns:
        Single most relevant document as dict, or None if no results
    """
    if not keywords:
        return None

    # Build optimized query
    query = " ".join(keywords)
    print(f"Search query: {query}")

    # Search and get more results for better BM25 scoring
    ddgs = DDGS()
    results = list(ddgs.text(query, region="us-es", max_results=10, backend=backend))

    if not results:
        return None

    # Find best document using BM25 scoring
    best_result = _find_best_document_bm25(results, keywords)

    if not best_result:
        return None

    # Add metadata
    best_result['search_keywords'] = keywords
    best_result['search_query'] = query

    # Small delay for rate limiting
    time.sleep(0.5)

    return best_result

def _find_best_document_bm25(results: List[Dict], keywords: List[str]) -> Optional[Dict]:
    """
    Use BM25 to find the most relevant document from search results using full HTML content.

    Args:
        results: List of search result dictionaries
        keywords: List of keywords to match against

    Returns:
        Best matching document or None
    """
    if not results or not keywords:
        return None

    # Prepare documents for BM25 (fetch HTML content for better scoring)
    documents = []
    valid_results = []

    for result in results:
        title = result.get('title', '')
        url = result.get('href', '')

        # Fetch and process HTML content
        html_content = _fetch_html_content(url)

        if html_content:
            # Weight title more heavily and combine with HTML content
            weighted_doc = f"{title} {html_content}"
            documents.append(weighted_doc)
            valid_results.append(result)
        else:
            # Fallback to snippet if HTML fetch fails
            snippet = result.get('body', '')
            weighted_doc = f"{title} {snippet}"
            documents.append(weighted_doc)
            valid_results.append(result)

    if not documents:
        return None

    # Tokenize documents and keywords
    tokenized_docs = [_tokenize_text(doc) for doc in documents]
    tokenized_keywords = []
    for keyword in keywords:
        tokenized_keywords.extend(_tokenize_text(keyword))

    # Remove duplicates while preserving order
    seen = set()
    unique_keywords = []
    for kw in tokenized_keywords:
        if kw not in seen:
            seen.add(kw)
            unique_keywords.append(kw)

    # Create BM25 index
    bm25 = BM25Okapi(tokenized_docs)

    # Calculate scores for each document
    scores = bm25.get_scores(unique_keywords)

    # Debug: show scores
    for i, (doc, score) in enumerate(zip(documents, scores)):
        print(f"Result {i}: {valid_results[i].get('title', '')[:50]}... | Score: {score:.4f}")

    # Find the document with highest score
    best_idx = max(range(len(scores)), key=lambda i: scores[i])
    best_result = valid_results[best_idx].copy()
    best_result['bm25_score'] = float(scores[best_idx])
    best_result['fetched_content'] = documents[best_idx][:5000]  # Limit content size

    return best_result


def _fetch_html_content(url: str) -> Optional[str]:
    """
    Fetch and extract text content from a webpage.

    Args:
        url: URL to fetch

    Returns:
        Cleaned text content or None if failed
    """
    if not url:
        return None

    try:
        # Fetch the webpage with timeout
        response = requests.get(url, timeout=10, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

        if response.status_code != 200:
            return None

        # Parse HTML and extract text
        soup = BeautifulSoup(response.content, 'html.parser')

        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()

        # Get text content
        text = soup.get_text()

        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)

        # Limit text length to avoid memory issues (first 5000 characters)
        return text[:5000] if text else None

    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None


def _tokenize_text(text: str) -> List[str]:
    """
    Simple tokenization for BM25.

    Args:
        text: Text to tokenize

    Returns:
        List of tokens
    """
    # Convert to lowercase and remove special characters
    text = re.sub(r'[^\w\s]', ' ', text.lower())
    # Split on whitespace and remove empty strings
    tokens = [token for token in text.split() if token]
    return tokens
