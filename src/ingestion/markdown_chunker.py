"""
Semantic Markdown Chunker for SAP ABAP Documentation

Downloads and chunks SAP ABAP cheat sheets with semantic awareness,
preserving headers and their associated code blocks.
"""

import re
import requests
from typing import List, Dict, Any
from dataclasses import dataclass


@dataclass
class DocumentChunk:
    """Represents a semantic chunk of a document."""
    content: str
    metadata: Dict[str, Any]
    
    def __repr__(self):
        return f"DocumentChunk(size={len(self.content)}, metadata={self.metadata})"


class MarkdownChunker:
    """
    Semantic chunker for Markdown documents.
    
    Uses header-based splitting to preserve context between headers
    and their associated content/code blocks.
    """
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def download_markdown(self, url: str) -> str:
        """
        Download raw markdown content from a URL.
        
        Args:
            url: Raw GitHub content URL or similar
            
        Returns:
            Raw markdown text
        """
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.text
    
    def chunk_markdown(self, text: str, source_url: str) -> List[DocumentChunk]:
        """
        Split markdown into semantic chunks based on headers.
        
        Args:
            text: Raw markdown text
            source_url: Original source URL for metadata
            
        Returns:
            List of DocumentChunk objects with metadata
        """
        chunks = []
        lines = text.split('\n')
        
        current_chunk_lines = []
        current_headers = []
        current_section = ""
        in_code_block = False
        code_block_content = []
        
        for line_num, line in enumerate(lines):
            # Track code blocks
            if line.strip().startswith('```'):
                if in_code_block:
                    # End of code block
                    code_block_content.append(line)
                    current_chunk_lines.extend(code_block_content)
                    code_block_content = []
                    in_code_block = False
                else:
                    # Start of code block
                    in_code_block = True
                    code_block_content = [line]
                continue
            
            if in_code_block:
                code_block_content.append(line)
                continue
            
            # Check for headers
            header_match = re.match(r'^(#{1,6})\s+(.+)$', line)
            if header_match:
                # Save previous chunk if it exists
                if current_chunk_lines:
                    chunk_text = '\n'.join(current_chunk_lines).strip()
                    if chunk_text:
                        chunks.append(DocumentChunk(
                            content=chunk_text,
                            metadata={
                                'source_url': source_url,
                                'headers': current_headers.copy(),
                                'section': current_section,
                                'chunk_index': len(chunks)
                            }
                        ))
                
                # Start new chunk with header
                level = len(header_match.group(1))
                title = header_match.group(2).strip()
                
                # Update header hierarchy
                current_headers = current_headers[:level-1]
                current_headers.append(title)
                current_section = title
                
                current_chunk_lines = [line]
            else:
                current_chunk_lines.append(line)
        
        # Don't forget the last chunk
        if current_chunk_lines:
            chunk_text = '\n'.join(current_chunk_lines).strip()
            if chunk_text:
                chunks.append(DocumentChunk(
                    content=chunk_text,
                    metadata={
                        'source_url': source_url,
                        'headers': current_headers.copy(),
                        'section': current_section,
                        'chunk_index': len(chunks)
                    }
                ))
        
        # Post-process: split large chunks while preserving code blocks
        final_chunks = self._split_large_chunks(chunks)
        
        return final_chunks
    
    def _split_large_chunks(self, chunks: List[DocumentChunk]) -> List[DocumentChunk]:
        """
        Split chunks that exceed chunk_size while trying to preserve
        semantic boundaries.
        """
        final_chunks = []
        
        for chunk in chunks:
            if len(chunk.content) <= self.chunk_size:
                final_chunks.append(chunk)
                continue
            
            # Split large chunks by paragraphs or code blocks
            parts = self._split_by_semantic_boundaries(chunk.content)
            
            current_part = ""
            part_index = 0
            
            for part in parts:
                if len(current_part) + len(part) > self.chunk_size and current_part:
                    # Save current part as a chunk
                    final_chunks.append(DocumentChunk(
                        content=current_part.strip(),
                        metadata={
                            **chunk.metadata,
                            'chunk_index': f"{chunk.metadata['chunk_index']}.{part_index}",
                            'is_subchunk': True
                        }
                    ))
                    # Start new part with overlap
                    current_part = current_part[-self.chunk_overlap:] if len(current_part) > self.chunk_overlap else ""
                    part_index += 1
                
                current_part += part
            
            # Don't forget the last part
            if current_part.strip():
                final_chunks.append(DocumentChunk(
                    content=current_part.strip(),
                    metadata={
                        **chunk.metadata,
                        'chunk_index': f"{chunk.metadata['chunk_index']}.{part_index}",
                        'is_subchunk': True
                    }
                ))
        
        return final_chunks
    
    def _split_by_semantic_boundaries(self, text: str) -> List[str]:
        """
        Split text by semantic boundaries (paragraphs, code blocks).
        """
        parts = []
        current_part = []
        in_code_block = False
        
        for line in text.split('\n'):
            if line.strip().startswith('```'):
                if in_code_block:
                    # End of code block
                    current_part.append(line)
                    parts.append('\n'.join(current_part) + '\n\n')
                    current_part = []
                    in_code_block = False
                else:
                    # Start of code block - save any accumulated text
                    if current_part:
                        parts.append('\n'.join(current_part) + '\n\n')
                        current_part = []
                    in_code_block = True
                    current_part.append(line)
            else:
                current_part.append(line)
        
        # Don't forget remaining content
        if current_part:
            parts.append('\n'.join(current_part) + '\n\n')
        
        return parts
    
    def process_url(self, url: str) -> List[DocumentChunk]:
        """
        Download and chunk markdown from a URL.
        
        Args:
            url: URL to download
            
        Returns:
            List of DocumentChunk objects
        """
        text = self.download_markdown(url)
        return self.chunk_markdown(text, url)


# SAP ABAP Cheat Sheet URLs
SAP_CHEAT_SHEET_URLS = [
    "https://raw.githubusercontent.com/SAP-samples/abap-cheat-sheets/main/README.md",
    "https://raw.githubusercontent.com/SAP-samples/abap-cheat-sheets/main/01_ABAP_SQL.md",
    "https://raw.githubusercontent.com/SAP-samples/abap-cheat-sheets/main/02_CDS.md",
    "https://raw.githubusercontent.com/SAP-samples/abap-cheat-sheets/main/03_RAP.md",
]


def download_and_chunk_sap_docs(urls: List[str] = None) -> List[DocumentChunk]:
    """
    Download and chunk all SAP ABAP cheat sheets.
    
    Args:
        urls: List of URLs to process (defaults to SAP_CHEAT_SHEET_URLS)
        
    Returns:
        Combined list of all document chunks
    """
    if urls is None:
        urls = SAP_CHEAT_SHEET_URLS
    
    chunker = MarkdownChunker()
    all_chunks = []
    
    for url in urls:
        try:
            chunks = chunker.process_url(url)
            all_chunks.extend(chunks)
        except Exception as e:
            print(f"Error processing {url}: {e}")
    
    return all_chunks


if __name__ == "__main__":
    # Test the chunker
    chunker = MarkdownChunker()
    
    # Test with a single URL
    test_url = SAP_CHEAT_SHEET_URLS[0]
    print(f"Downloading and chunking: {test_url}")
    
    chunks = chunker.process_url(test_url)
    print(f"Generated {len(chunks)} chunks")
    
    # Show first chunk
    if chunks:
        print(f"\nFirst chunk preview:")
        print(f"Metadata: {chunks[0].metadata}")
        print(f"Content (first 500 chars): {chunks[0].content[:500]}...")
