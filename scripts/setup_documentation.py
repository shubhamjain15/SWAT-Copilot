"""
Script to set up SWAT documentation indexing.

Usage:
    python scripts/setup_documentation.py [--yes]
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from swat_copilot.llm.rag import SWATRAGSystem


def main():
    """Set up documentation index."""
    print("=== SWAT Documentation Setup ===\n")

    # Documentation path
    docs_path = Path(__file__).parent.parent / "docs" / "swat_documentation"

    print(f"Documentation folder: {docs_path}")
    print(f"Looking for PDFs in: {docs_path / 'pdfs'}")
    print(f"Looking for text files in: {docs_path / 'text'}\n")

    # Check if documentation exists
    if not docs_path.exists():
        print("⚠️  Documentation folder not found!")
        print(f"Creating folder structure at: {docs_path}")
        docs_path.mkdir(parents=True, exist_ok=True)
        (docs_path / "pdfs").mkdir(exist_ok=True)
        (docs_path / "text").mkdir(exist_ok=True)
        print("\n✅ Folders created!")
        print(f"\nNext steps:")
        print(f"1. Add your SWAT PDF files to: {docs_path / 'pdfs'}")
        print(f"2. Add any text documentation to: {docs_path / 'text'}")
        print(f"3. Run this script again to build the index")
        return

    # Count files
    pdf_files = list((docs_path / "pdfs").glob("*.pdf")) if (docs_path / "pdfs").exists() else []
    txt_files = list((docs_path / "text").glob("*.txt")) if (docs_path / "text").exists() else []

    print(f"Found {len(pdf_files)} PDF files")
    print(f"Found {len(txt_files)} text files\n")

    if not pdf_files and not txt_files:
        print("⚠️  No documentation files found!")
        print(f"\nPlease add files to:")
        print(f"  - PDFs: {docs_path / 'pdfs'}")
        print(f"  - Text: {docs_path / 'text'}")
        return

    # List files
    if pdf_files:
        print("PDF files:")
        for f in pdf_files:
            size_mb = f.stat().st_size / (1024 * 1024)
            print(f"  - {f.name} ({size_mb:.1f} MB)")

    if txt_files:
        print("\nText files:")
        for f in txt_files:
            size_kb = f.stat().st_size / 1024
            print(f"  - {f.name} ({size_kb:.1f} KB)")

    # Build index
    print("\n" + "="*50)

    # Check for --yes flag
    auto_yes = "--yes" in sys.argv or "-y" in sys.argv

    if not auto_yes:
        response = input("\nBuild documentation index? This may take a few minutes. (y/n): ")
        if response.lower() != 'y':
            print("Cancelled.")
            return

    print("\nBuilding index...")
    print("This will:")
    print("1. Load all PDF and text files")
    print("2. Split them into chunks")
    print("3. Create vector embeddings")
    print("4. Save to a searchable database\n")

    try:
        rag = SWATRAGSystem(documentation_path=docs_path)
        rag.build_index()
        print("\n✅ Index built successfully!")
        print(f"Index saved to: {docs_path / 'vector_index'}")

        # Test search
        print("\n" + "="*50)
        print("Testing search...")
        test_query = "What is SWAT?"
        results = rag.retrieve_context(test_query, top_k=1)

        if results:
            print(f"\nTest query: '{test_query}'")
            print(f"Found {len(results)} result(s)")
            print(f"\nFirst result (from {results[0]['source']}):")
            print(results[0]['text'][:200] + "...")
        else:
            print("No results found")

        print("\n✅ Setup complete! Documentation is ready to use.")

    except ImportError as e:
        print(f"\n❌ Error: Missing dependencies")
        print(f"\nPlease install required packages:")
        print("pip install langchain langchain-community chromadb pypdf sentence-transformers")
        print(f"\nError details: {e}")
    except Exception as e:
        print(f"\n❌ Error building index: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
