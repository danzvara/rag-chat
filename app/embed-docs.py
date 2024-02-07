import os
from pathlib import Path
from langchain.text_splitter import HTMLHeaderTextSplitter
from slugify import slugify

from pinecone import Pinecone, PodSpec
from langchain.vectorstores.pinecone import Pinecone as LangchainPinecone
from langchain_openai import OpenAIEmbeddings

from dotenv import load_dotenv

load_dotenv()


def create_documents_from_html_page(page_file: Path):
    """Creates documents from the given html page file."""

    if not str(page_file).endswith(".html"):
        raise ValueError("The given file is not an HTML file.")

    headers_to_split_on = [
        ("h1", "h1"),
        ("h2", "h2"),
        ("h3", "h3"),
    ]
    versions = ["v2.0.0", "v2.1.0", "v2.1.1", "main"]

    html_splitter = HTMLHeaderTextSplitter(headers_to_split_on)
    header_splits = html_splitter.split_text_from_file(page_file)

    sections = list(filter(lambda section: "h1" in section.metadata, header_splits))

    for section in sections:
        for header in headers_to_split_on[::-1]:
            if header[0] in section.metadata:
                header_text = section.metadata[header[0]]
                break

        if header_text:
            section.page_content = header_text.strip("#") + "\n" + section.page_content
            section.metadata["path"] = (
                f"https://{str(page_file)}#{slugify(header_text, separator='-')}"
            )
        else:
            section.metadata["path"] = f"https://{str(page_file)}"

        version = [v for v in versions if v in section.metadata["path"]][0]
        section.metadata["version"] = version

    return sections


def create_documents(page_files):
    """Creates documents from the given list of page files."""

    # Having a bit of fun with list comprehensions here
    return [doc for page in page_files for doc in create_documents_from_html_page(page)]


# Using default ada-002 embedding model
embeddings = OpenAIEmbeddings()


if __name__ == "__main__":
    docs_dir = "docs/"
    os.chdir(docs_dir)
    with Path(".") as search_path:
        docs_pages = list(search_path.rglob("*.html"))

    # Exclude module files, we don't want to index source code of the SDK
    docs_pages = list(filter(lambda p: "_modules" not in str(p), docs_pages))

    documents = create_documents(docs_pages)

    pinecone = Pinecone()
    index_name = os.environ.get("PINECONE_INDEX_NAME")
    if index_name not in pinecone.list_indexes():
        pinecone.create_index(
            name=index_name,
            # 1536 is the default dimension for the ada-002 model
            dimension=1536,
            # Cosine similarity is the recommended metric for the ada-002 model
            # We're comparing semantic similarity of documents, not magnitude
            # (like in images for example), so cosine similarity seems most appropriate
            metric="cosine",
            spec=PodSpec(environment="gcp-starter"),
        )

    docsearch = LangchainPinecone.from_documents(
        documents, embeddings, index_name=index_name
    )
