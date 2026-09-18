#!/usr/bin/env python3
import os
import time
import yaml
import hashlib
import uuid
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
try:
    import pdfplumber
except ImportError:
    print("pdfplumber not installed")
    pdfplumber = None

PKC_MANIFEST = "pkc_manifest.yml"
ZOTERO_DIR = "research/zotero_attachments"

def process_pdf(file_path):
    print(f"Processing new PDF: {file_path}")
    if not pdfplumber:
        print("pdfplumber not available, skipping text extraction")
        return

    try:
        with pdfplumber.open(file_path) as pdf:
            text = "\n".join(page.extract_text() for page in pdf.pages[:3] if page.extract_text())

        print(f"Extracted {len(text)} characters from {file_path}")

        # Simulate local LLM extraction for metadata
        title = os.path.basename(file_path).replace('.pdf', '').replace('_', ' ').title()

        # Calculate SHA256
        with open(file_path, 'rb') as f:
            sha256 = hashlib.sha256(f.read()).hexdigest()

        # Add to manifest
        if os.path.exists(PKC_MANIFEST):
            with open(PKC_MANIFEST, 'r') as f:
                manifest = yaml.safe_load(f)

            new_node_uuid = f"urn:uuid:{uuid.uuid4()}"
            new_node = {
                "node_uuid": new_node_uuid,
                "title": title,
                "content_path": file_path,
                "node_type": "PDF_Atom",
                "status": "transient",
                "version_number": 1,
                "epistemic_tag": "hypothetical",
                "meaning_space_anchor": {
                    "prototypical_vector": [0.0, 0.0, 0.0, 0.0, 0.0],
                    "hyperspherical_radius": 0.1,
                    "embedding_model": "text-embedding-3-small"
                },
                "metadata_fields": {
                    "epistemic_risk_level": "Medium",
                    "architectural_layer": "Data_Ingestion",
                    "implementation_horizon": "TBD"
                }
            }

            if 'content_nodes' not in manifest:
                manifest['content_nodes'] = []
            manifest['content_nodes'].append(new_node)

            if 'metadata' in manifest and 'context_hashes' in manifest['metadata']:
                manifest['metadata']['context_hashes'].append(f"{file_path}:sha256-{sha256}")

            with open(PKC_MANIFEST, 'w') as f:
                yaml.safe_dump(manifest, f, default_flow_style=False)

            print(f"Added {title} to PKC Manifest with UUID {new_node_uuid}")

    except Exception as e:
        print(f"Error processing {file_path}: {e}")

class ZoteroHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith('.pdf'):
            # Allow time for file to be fully written
            threading.Timer(2.0, process_pdf, args=(event.src_path,)).start()

def main():
    if not os.path.exists(ZOTERO_DIR):
        os.makedirs(ZOTERO_DIR)

    observer = Observer()
    event_handler = ZoteroHandler()
    observer.schedule(event_handler, ZOTERO_DIR, recursive=True)

    print(f"Watching {ZOTERO_DIR} for new PDFs...")
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()
