# AI Employee for QA on Welfare Service Guidebook

## Ideas

- Langchain으로 Hallucination 탐지
- 지니랩스 tts, sst로 배리어프리 App 구현?
- IR의 경우, first stage + reranking으로 구현
- gpt api 중에 **text embedding**이 있음
  - 복지 제도 400개를 미리 embedding해두고 user query와 가장 유사한 복지 제도를 찾는 방식

## Links

### Postings

[개발자로서 LLM 사용을 위해 알아두면 좋은 내용들](https://haandol.github.io/2023/05/02/llm-for-ordinary-developers.html#fn:13)

- koAlpaca 사용시 유용한 내용들 다수 포함
- 미세 조정, 프롬프트 등등

[Prompt Engineering Guide](https://www.promptingguide.ai/)

- 프롬프트 엔지니어링 가이드

### LLMs

[koAlpaca 조금 써본 거](https://chat.koalpaca.com/r/2xWRgdz)

- fine tuning 없이는 그닥

[gpt3.5 조금 써본 거](https://chat.openai.com/share/381216b5-a797-4279-846a-8c92fc744cd3)

- 코알파카보다 훨씬 잘하는데 API만 활용해도 충분할 것 같다.
- 과장 좀 보태면 목요일까지 프로토타입 만들기 가능...

### Info Retrieval

[awesome-information-retrieval](https://github.com/harpribot/awesome-information-retrieval)

[awesome-pretrained-models-for-information-retrieval](https://github.com/ict-bigdatalab/awesome-pretrained-models-for-information-retrieval)

## Commit Message Convention

1. emoji \[type\] message

```
✨ [Add] Add html cleansing code
✨ [Add] Data preprocessing code
🐛 [Fix] Fix bugs
🛠️ [Git] resolve merge conflict
🛠️ [Git] .gitignore
✨ [Feat] Implement main logics (incomplete)
📝 [Docs] Update git files
📝 [Docs] Add TODO
🪮 [Style] Fix typo
```

2. type

```
✨ Feat : 새로운 기능 추가
✨ Add : 기능은 아닌 코드 추가
🐛 Fix : 버그 수정
📝 Docs : 문서 수정
🪮 Style : 코드 포맷팅, 세미콜론 누락, 코드 리프랙터, 코드 변경이 없는 경우
🛠️ Git : 깃허브 관련
```

3. message

- 첫글자는 대문자로 시작
- 필요한 경우 message 아래에 내용 첨부

```
Ex
✨ [Feat] Implement main logics (incomplete)

TODO
- vehicle_update 함수 수정 필요
- request_time 변수 추가 필요
- calculate_time unit test
```

## papers

- [Generation-Augmented Retrieval for Open-Domain Question Answering](https://arxiv.org/pdf/2009.08553.pdf)

- [Enhancing Retrieval-Augmented Large Language Models with Iterative Retrieval-Generation Synergy](https://arxiv.org/pdf/2305.15294.pdf)
