"""
Knowledge Base Extraction Script
Processes PDFs from assets/pdfs/cursuri/ and extracts concepts/definitions.
Supports both Romanian and English PDFs with automatic translation.
"""
import os
import sys
import json
import re
from pathlib import Path
from typing import List, Dict, Optional

# Add project root to sys.path for imports
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from utils.pdf_parser import extract_text_from_pdf
from utils.text_cleaner import clean_raw_text

try:
    from deep_translator import GoogleTranslator
    TRANSLATOR_AVAILABLE = True
except ImportError:
    TRANSLATOR_AVAILABLE = False
    print("Warning: deep-translator not installed. Translation will be skipped.")
    print("Install with: pip install deep-translator")


# Language detection patterns based on filename
ROMANIAN_INDICATORS = ['CSP', 'Ro', 'RO']
ENGLISH_INDICATORS = ['GT', 'SBM', 'IA_', 'EN', 'En']

# Concept extraction patterns
ROMANIAN_PATTERNS = [
    r'(Definiție|Definitie|DEFINIȚIE|DEFINITIE)\s*:?\s*(.+?)(?=\n\n|\n[A-Z]|$)',
    r'(Algoritmul|ALGORITMUL)\s+([A-Za-z0-9\-]+)\s*:?\s*(.+?)(?=\n\n|\n[A-Z]|$)',
    r'(Observație|Observatie|OBSERVAȚIE|OBSERVATIE)\s*:?\s*(.+?)(?=\n\n|\n[A-Z]|$)',
    r'(Teorema|TEOREMA)\s+([A-Za-z0-9\.\-]+)?\s*:?\s*(.+?)(?=\n\n|\n[A-Z]|$)',
]

ENGLISH_PATTERNS = [
    r'(Definition)\s*:?\s*(.+?)(?=\n\n|\n[A-Z]|$)',
    r'(Algorithm)\s+([A-Za-z0-9\-]+)\s*:?\s*(.+?)(?=\n\n|\n[A-Z]|$)',
    r'(Theorem)\s+([A-Za-z0-9\.\-]+)?\s*:?\s*(.+?)(?=\n\n|\n[A-Z]|$)',
    r'(Remark)\s*:?\s*(.+?)(?=\n\n|\n[A-Z]|$)',
]


def detect_language(filename: str) -> str:
    """
    Detect language based on filename patterns.
    
    Args:
        filename: Name of the PDF file
        
    Returns:
        'ro' for Romanian, 'en' for English
    """
    filename_upper = filename.upper()
    
    # Check Romanian indicators
    if any(indicator in filename_upper for indicator in ROMANIAN_INDICATORS):
        return 'ro'
    
    # Check English indicators
    if any(indicator in filename_upper for indicator in ENGLISH_INDICATORS):
        return 'en'
    
    # Default to Romanian
    return 'ro'


def translate_to_romanian(text: str) -> str:
    """
    Translate English text to Romanian using Google Translator.
    
    Args:
        text: English text to translate
        
    Returns:
        Translated Romanian text or original if translation fails
    """
    if not TRANSLATOR_AVAILABLE:
        return text
    
    try:
        translator = GoogleTranslator(source='en', target='ro')
        # Split long text into chunks (Google Translate has 5000 char limit)
        max_chunk_size = 4500
        
        if len(text) <= max_chunk_size:
            return translator.translate(text)
        
        # Split into sentences and translate in chunks
        sentences = re.split(r'(?<=[.!?])\s+', text)
        translated_chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            if len(current_chunk) + len(sentence) < max_chunk_size:
                current_chunk += sentence + " "
            else:
                if current_chunk:
                    translated_chunks.append(translator.translate(current_chunk.strip()))
                current_chunk = sentence + " "
        
        if current_chunk:
            translated_chunks.append(translator.translate(current_chunk.strip()))
        
        return " ".join(translated_chunks)
    
    except Exception as e:
        print(f"  ⚠️  Translation failed: {e}")
        return text


def extract_concepts_from_text(text: str, language: str) -> List[Dict[str, str]]:
    """
    Extract concepts (definitions, algorithms, theorems) from text.
    
    Args:
        text: Cleaned text from PDF
        language: 'ro' or 'en'
        
    Returns:
        List of concept dictionaries
    """
    concepts = []
    patterns = ROMANIAN_PATTERNS if language == 'ro' else ENGLISH_PATTERNS
    
    # Clean text for better pattern matching
    text = re.sub(r'\s+', ' ', text)  # Normalize whitespace
    
    for pattern in patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE | re.DOTALL)
        
        for match in matches:
            groups = match.groups()
            
            # Extract concept type and content
            if len(groups) == 2:
                concept_type, content = groups
                concept_name = None
            else:
                concept_type = groups[0]
                concept_name = groups[1] if groups[1] else None
                content = groups[2] if len(groups) > 2 else groups[1]
            
            # Clean content
            content = content.strip()
            if len(content) < 10:  # Skip very short matches
                continue
            
            # Build concept dictionary
            concept = {
                'type': concept_type.strip(),
                'content': content[:500],  # Limit to 500 chars
            }
            
            if concept_name:
                concept['name'] = concept_name.strip()
            
            concepts.append(concept)
    
    return concepts


def process_single_pdf(pdf_path: Path, language: str) -> List[Dict[str, str]]:
    """
    Process a single PDF file and extract knowledge.
    
    Args:
        pdf_path: Path to PDF file
        language: Detected language ('ro' or 'en')
        
    Returns:
        List of extracted concepts with metadata
    """
    print(f"\n{'='*60}")
    print(f"Processing: {pdf_path.name}")
    print(f"Language: {'Romanian' if language == 'ro' else 'English'}")
    print('='*60)
    
    # Extract text
    raw_text = extract_text_from_pdf(str(pdf_path))
    
    if "Eroare:" in raw_text:
        print(f"  ❌ {raw_text}")
        return []
    
    print(f"  ✓ Text extracted ({len(raw_text)} characters)")
    
    # Clean text
    clean_text = clean_raw_text(raw_text)
    print(f"  ✓ Text cleaned ({len(clean_text)} characters)")
    
    # Extract concepts
    concepts = extract_concepts_from_text(clean_text, language)
    print(f"  ✓ Found {len(concepts)} concepts")
    
    # Translate if English
    if language == 'en' and TRANSLATOR_AVAILABLE and concepts:
        print(f"  🔄 Translating to Romanian...")
        for concept in concepts:
            original_content = concept['content']
            concept['content'] = translate_to_romanian(original_content)
            concept['original_content'] = original_content
            concept['translated'] = True
        print(f"  ✓ Translation complete")
    
    # Add metadata
    for concept in concepts:
        concept['source'] = pdf_path.name
        concept['language'] = language
    
    return concepts


def build_knowledge_base():
    """
    Main function to build the knowledge base from all PDF files.
    """
    print("\n" + "="*60)
    print("  KNOWLEDGE BASE EXTRACTION")
    print("="*60)
    
    # Paths
    cursuri_dir = project_root / "assets" / "pdfs" / "cursuri"
    output_dir = project_root / "assets" / "json_output"
    output_file = output_dir / "knowledge_base.json"
    
    # Check if cursuri directory exists
    if not cursuri_dir.exists():
        print(f"\n❌ Directory not found: {cursuri_dir}")
        return
    
    # Find all PDFs
    pdf_files = sorted(cursuri_dir.glob("*.pdf"))
    
    if not pdf_files:
        print(f"\n❌ No PDF files found in {cursuri_dir}")
        return
    
    print(f"\n📄 Found {len(pdf_files)} PDF files\n")
    
    # Process all PDFs
    all_concepts = []
    stats = {'ro': 0, 'en': 0, 'total_concepts': 0}
    
    for pdf_path in pdf_files:
        language = detect_language(pdf_path.name)
        stats[language] += 1
        
        concepts = process_single_pdf(pdf_path, language)
        all_concepts.extend(concepts)
        stats['total_concepts'] += len(concepts)
    
    # Save to JSON
    output_dir.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_concepts, f, ensure_ascii=False, indent=2)
    
    print("\n" + "="*60)
    print("  EXTRACTION COMPLETE")
    print("="*60)
    print(f"\n📊 Statistics:")
    print(f"   Romanian PDFs: {stats['ro']}")
    print(f"   English PDFs: {stats['en']}")
    print(f"   Total Concepts: {stats['total_concepts']}")
    print(f"\n✅ Knowledge base saved to: {output_file}")
    print("="*60 + "\n")


if __name__ == "__main__":
    build_knowledge_base()
