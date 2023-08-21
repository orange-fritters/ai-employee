# AI-Employee

## Introduction
This project is about building a closed domain question answering chat bot which answers questions asked by users who are looking for welfare service.

AI-employee retrieve information from the 400 pages sized welfare-service-guide-book and answers the question.

- Basic version : Retrieve, Question Answering
- Advanced version : +Multiturn recommendation system

## Demo

## Explanation

### Installation 

> Go to [SETUP.md](SETUP.md)

### Code

#### frontend/src

- `App.tsx` : Main component
- `Main.tsx` : Main page, contains `Header`, `SearchBar`, `Message`, `Button`
- `components` : Contains `Button`, `Header`, `Message`, `SearchBar`
  - `styles` : styled-components for each component, **design changes** should be made here
  - `Button.tsx` 
    - Two types of Button, (1) Search Button (2) Recommendation Button
    - Search Button : `utils/handleButton/handleSearchButton` function is called when clicked and goes back to initial state
    - Recommendation Button : `utils/handleButton/handleRecommendationButton` function is called when clicked and renders recommendation message which is stored in `redux/recommendation.slice`. Show clickable four recommendated services.
  - `Header.tsx` : Header component
  - `Message.tsx` : Message component, 5 types of messages, varying with the buttons attached, what to show.
  - `SearchBar.tsx` : SearchBar component, `utils/handleSubmit.ts` function which is called when user types in the search bar and press enter. Defined with two states, when `search` or additional `ask`. Component sends request to the server and receive response from the server.
- `redux`
  - Contains `defaultMessages`, `message.slice`, `recommendation.slice`, `selectors`, `store`
  - handles state management with redux-toolkit slicers
    - Slicers are state management tool which is able to handle state and action in a single file with less code
  - When states inside redux-store changes, components are re-rendered 
- `requests`
  - Contains `requestQuery`, `requestRecommendation`, `requestSearch`, `requestSummary`, `streamResponse`
  - `requestQuery` : ask and answer based on single document
  - `requestRecommendation` : receive recommendation based on single query
  - `requestSearch` : send query to the server and receive response with 5 documents
  - `requestSummary` : send query to the server and receive pregenerated summary 
  - `streamResponse` : with a response from the server, stream the response to the frontend (word by word text message)
- `utils`
  - `decoder.ts` : decode the response from the server (byte to string)
  - `handleButton.ts` : handle button click event using slicers!
  - `handleRecommendation.ts` : handle recommendation state using slicers!
  - `handleSubmit.ts` : handle submit event using slicers!

#### server
- `articles`
  - Contains 462 preprocessed html files
- `model`
  - `model/bm25` 
    - `bm25.py` : bm25 model
    - `model.py` : final model using bm25
  - `model/neural_model`
    - `neural_model.py` : neural model, but not used in the compact-version
  - `model/files`
    - Contains preprocessed data
    - `info_sheet.csv` : contains information about each document
    - `processed_doc.csv` : contains preprocessed document in English, keywords and summary included.
  - `model/utils`
    - `convert_prompt.py` : convert to prompt
    - `get_chat.py` : get chat from openai, **modify when migrate**
    - `get_response_openai.py` : get response from openai, **modify when migrate** little bit different from `get_chat.py`
    - `schemas.py` : schemas for server
  - `io_model.py` : io model, handles input and output, basic file handling
- `server.py` : server, handles request and response  
  - `../frontend/build` : build folder of react app. render static files made with react are rendered here.
  - contains various endpoints.




## Project tree
```
.
├── README.md
├── config.txt
├── frontend
│   ├── README.md
│   ├── build
│   ├── package.json
│   ├── public
│   ├── src
│   │   ├── App.css
│   │   ├── App.js
│   │   ├── Main.tsx
│   │   ├── components
│   │   │   ├── Button.tsx
│   │   │   ├── Header.tsx
│   │   │   ├── Message.tsx
│   │   │   ├── SearchBar.tsx
│   │   │   └── styles
│   │   │       ├── Button.style.ts
│   │   │       ├── Header.style.ts
│   │   │       ├── Main.style.ts
│   │   │       ├── Message.style.ts
│   │   │       ├── SearchBar.style.ts
│   │   │       └── styles.ts
│   │   ├── index.css
│   │   ├── index.js
│   │   ├── react-app-env.d.ts
│   │   ├── redux
│   │   │   ├── defaultMessages.ts
│   │   │   ├── message.slice.ts
│   │   │   ├── recommendation.slice.ts
│   │   │   ├── selectors.ts
│   │   │   └── store.ts
│   │   ├── requests
│   │   │   ├── requestQuery.ts
│   │   │   ├── requestRecommendation.ts
│   │   │   ├── requestSearch.ts
│   │   │   ├── requestSummary.ts
│   │   │   └── streamResponse.ts
│   │   └── utils
│   │       ├── decoder.ts
│   │       ├── handleButton.ts
│   │       ├── handleRecommendation.ts
│   │       └── handleSubmit.ts
│   └── tsconfig.json
├── server
│   ├── Dockerfile
│   ├── articles
│   │   ├── tokenized_articles
│   │   │   └── html.pkl
│   │   ├── 기타지원_01.html
│   │   ├── 기타지원_02.html
│   │   ├── ...
│   │   ├── 취업지원_34.html
│   │   ├── 취업지원_35.html
│   │   └── 취업지원_36.html
│   ├── config.json
│   ├── model
│   │   ├── bm25
│   │   │   ├── articles_preprocessed.pkl
│   │   │   ├── bm25.py
│   │   │   ├── ensemble.py
│   │   │   ├── html_preprocess.py
│   │   │   ├── query_expansion.py
│   │   │   ├── text_preprocess.py
│   │   │   └── word_similarity.pkl
│   │   ├── files
│   │   │   ├── articles_eng.parquet
│   │   │   ├── info_sheet.csv
│   │   │   └── processed_doc.csv
│   │   ├── io_model.py
│   │   ├── neural_model
│   │   │   ├── exceptions.py
│   │   │   ├── neural_base.py
│   │   │   ├── neural_model.py
│   │   │   └── prompts.py
│   │   └── utils
│   │       ├── convert_prompt.py
│   │       ├── get_chat.py
│   │       ├── get_response_openai.py
│   │       └── schemas.py
│   ├── requirements.txt
│   └── server.py
└── server.sh
```

## 