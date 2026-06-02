from __future__ import annotations

import csv
import io
import re
from pathlib import Path
from typing import Iterable

from docx import Document as DocxDocument
from pypdf import PdfReader


class IngestionError(ValueError):
    pass


class DocumentIngestionService:
    def extract_text(self, file_path: str, mime_type: str) -> str:
        suffix = Path(file_path).suffix.lower()
        if mime_type == "application/pdf" or suffix == ".pdf":
            return self._extract_pdf(file_path)
        if mime_type in {"application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/msword"} or suffix in {".docx", ".doc"}:
            return self._extract_docx(file_path)
        if mime_type == "text/csv" or suffix == ".csv":
            return self._extract_csv(file_path)
        if mime_type.startswith("text/") or suffix in {".txt", ".md"}:
            return Path(file_path).read_text(encoding="utf-8", errors="ignore")
        raise IngestionError(f"Unsupported file type: {mime_type}")

    def _extract_pdf(self, file_path: str) -> str:
        reader = PdfReader(file_path)
        return "\n".join(page.extract_text() or "" for page in reader.pages)

    def _extract_docx(self, file_path: str) -> str:
        document = DocxDocument(file_path)
        return "\n".join(paragraph.text for paragraph in document.paragraphs)

    def _extract_csv(self, file_path: str) -> str:
        rows: list[str] = []
        with open(file_path, newline="", encoding="utf-8") as handle:
            reader = csv.reader(handle)
            for row in reader:
                rows.append(" | ".join(row))
        return "\n".join(rows)

    def chunk_text(self, text: str, max_chars: int = 1200, overlap: int = 200) -> list[str]:
        normalized = re.sub(r"\s+", " ", text).strip()
        if not normalized:
            return []
        chunks: list[str] = []
        start = 0
        while start < len(normalized):
            end = min(len(normalized), start + max_chars)
            chunks.append(normalized[start:end])
            if end == len(normalized):
                break
            start = max(0, end - overlap)
        return chunks