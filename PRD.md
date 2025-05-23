# **Project Requirements Document: Accent Analysis Tool**

The following table outlines the detailed functional requirements of the Accent Analysis Tool.

| Requirement ID | Description               | User Story                                                                                       | Expected Behavior/Outcome                                                                                                     |
|-----------------|---------------------------|--------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------|
| FR001          | Video URL Input          | As a user, I want to be able to input a public video URL (Loom or MP4) so I can analyze the speaker's accent. | The system should provide an input field for users to enter video URLs and validate the input format. |
| FR002          | Audio Extraction         | As a user, I want the system to automatically extract audio from the video so it can be analyzed. | The system should process the video URL and extract the audio track for further analysis. |
| FR003          | Accent Classification    | As a user, I want to know what type of English accent the speaker has (British, American, Australian, etc.). | The system should analyze the audio and classify the accent type with a clear label. |
| FR004          | Confidence Scoring       | As a user, I want to see how confident the system is about the accent classification. | The system should provide a confidence score (0-100%) for the accent classification. |
| FR005          | Analysis Summary         | As a user, I want to understand why the system classified the accent in a particular way. | The system should provide a brief explanation of the accent classification decision. |
| FR006          | English Accent Focus     | As a user, I want to ensure the system only analyzes English accents for hiring purposes. | The system should be specifically trained and optimized for English accent detection. |
| FR007          | User Interface           | As a user, I want a simple and intuitive interface to interact with the tool. | The system should provide a clean UI (CLI, Streamlit, or Flask) for easy interaction. |


## Technical Requirements

1. **Input Processing**
   - Support for Loom video URLs
   - Support for direct MP4 video links
   - Input validation and error handling

2. **Audio Processing**
   - Efficient audio extraction from video
   - Audio format conversion if needed
   - Handling of various video formats

3. **Accent Analysis**
   - English accent classification
   - Confidence scoring system
   - Analysis explanation generation

## Success Criteria

1. **Functional Requirements**
   - Must successfully process video URLs
   - Must accurately classify English accents
   - Must provide confidence scores
   - Must include explanation of results


## Evaluation Criteria

1. **Must-Have (Pass)**
   - Working script that returns accent classification
   - Logical approach using valid methods
   - Clear setup instructions
   - English accent handling

## Overview
Accent Analyzer is an AI-powered tool designed to evaluate English language accents from video content. It assists in the hiring process by providing objective accent analysis and English proficiency scoring.

## Problem Statement
HR teams and recruiters need an efficient, unbiased way to evaluate candidates' English speaking abilities and accent clarity during the hiring process. Manual assessment is time-consuming and can be subjective.

## Objectives
- Provide automated accent analysis from video content
- Deliver objective scoring for English language proficiency
- Streamline the candidate evaluation process
- Ensure fair and consistent assessment

## Features

### Must Have (MVP)
1. Video Input Processing
   - Accept public video URLs (Loom, direct MP4)
   - Support for common video formats
   - Video length limit: 5 minutes

2. Audio Extraction
   - Clean audio isolation from video
   - Noise reduction
   - Format standardization

3. Accent Analysis
   - Detection of major English accents:
     - American
     - British
     - Australian
     - Canadian
   - Confidence score (0-100%)


## Success Criteria
1. Success
   - Reliable accent detection
   - Accurate confidence scoring
   - Stable system performance
