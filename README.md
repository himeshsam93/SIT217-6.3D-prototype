# SIT217-6.3D-prototype

This repository contains the prototype implementation of an Automated Requirement Extraction System (ARES) designed to process unstructured business documents and extract functional, non-functional, and business requirements automatically. The system leverages Natural Language Processing (NLP) techniques to identify requirement-like sentences, classify them, flag ambiguous terms, and maintain traceability to the original sources.

Key Features

Upload and analyze business documents in multiple formats (e.g., DOCX, PDF, TXT).
Automatic identification of requirement sentences using imperative keywords (must, shall, should).
Classification of requirements into Functional Requirements (FR), Non-Functional Requirements (NFR), and Business Requirements (BR).
Ambiguity detection and highlighting for terms like fast, efficient, secure.
Traceability mapping linking each requirement to its source document.
Export of structured requirements to tools such as Excel, Jira, or IBM DOORS.
Human-in-the-loop review for analysts to verify and refine extracted requirements.

Technologies Used

Python 3.x
Natural Language Processing: spaCy, NLTK
Data handling: pandas
Document processing: python-docx, PyPDF2
