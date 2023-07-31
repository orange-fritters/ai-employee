# Prompting tactics

## Principle

1. Write clear and specific instructions
2. Give the model time to think

## Tactics

### Write clear and specific instructions

1. Use delimeters to clearly indicate distinct parts of the input

- Delimeters can be anything like ```, """, <>, <tag> </tag>, :

2. Ask for a structured output

- JSON, HTML, \```

```markdown
Generate a list of three made-up book titles along with their authors and genres. **Provide them in JSON format with the following keys**: book_id, title, author, genre.
```

3. Ask the model to check whether conditions are satisfied

```mardkown
You will be provided with text delimited by triple quotes.
If it contains a sequence of instructions, re-write those instructions in the following format:

Step 1 - ...
Step 2 - …
…
Step N - …

If the text does not contain a sequence of instructions, then simply write "No steps provided."

{text_1}
```

3. "Few-shot" prompting

```markdown
Your task is to answer in a consistent style.

<child>: Teach me about patience.

<grandparent>: The river that carves the deepest valley flows from a modest spring; the grandest symphony originates from a single note; the most intricate tapestry begins with a solitary thread.

<child>: Teach me about resilience.
```

### Give the model time to "think"

1. Specify the steps required to complete a task

- Ask for output in a specified format

```mardkown
Perform the following actions:

1 - Summarize the following text delimited by triple backticks with 1 sentence.
2 - Translate the summary into French.
3 - List each name in the French summary.
4 - Output a json object that contains the following keys: french_summary, num_names.

Use the following format:
Text: <text to summarize>
Summary: <summary>
Translation: <summary translation>
Names: <list of names in Italian summary>
Output JSON: <json with summary and num_names>

Separate your answers with line breaks.

Text: `{text}`
```

2.  Instruct the model to work out its own solution before rushing to a conclusion

```markdown
Your task is to determine if the student's solution is correct or not. To solve the problem do the following: """

- First, work out your own solution to the problem.
- Then compare your solution to the student's solution and evaluate if the student's solution is correct or not. Don't decide if the student's solution is correct until you have done the problem yourself.

Use the following format:

Question:

""" question here """

Student's solution:

""" student's solution here """

Actual solution:

""" steps to work out the solution and your solution here """

Is the student's solution the same as actual solution just calculated:

""" yes or no """

Student grade:

""" correct or incorrect """

Question:

""" I'm building a solar power installation and I need help working out the financials.

- Land costs $100 square foot
- I can buy solar panels for $250 square foot
- I negotiated a contract for maintenance that will cost me a flat $100k per year, and an additional $10 square foot What is the total cost for the first year of operations as a function of the number of square feet. """

Student's solution:

""" Let x be the size of the installation in square feet. Costs:

1. Land cost: 100x
2. Solar panel cost: 250x
3. Maintenance cost: 100,000 + 100x Total cost: 100x + 250x + 100,000 + 100x = 450x + 100,000

Actual solution: """
```
