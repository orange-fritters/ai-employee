import os
from bs4 import BeautifulSoup, NavigableString

# Create the output directory if it doesn't exist
output_dir = 'data/notags'
os.makedirs(output_dir, exist_ok=True)

# Process each file in the input directory
input_dir = 'data/articles'
for i, filename in enumerate(sorted(os.listdir(input_dir))):
    input_file = os.path.join(input_dir, filename)
    output_file = os.path.join(output_dir, filename)

    # Read the input file
    with open(input_file, 'r') as f:
        content = f.read()

    # Parse the HTML content
    soup = BeautifulSoup(content, 'html.parser')

    # Remove all HTML tags and leave only the text
    text = ''.join([text for text in soup.recursiveChildGenerator() if isinstance(text, NavigableString)]).strip()

    # Remove spaces longer than a single space
    text = ' '.join(text.split())

    # Write the text to the output file
    with open(output_file, 'w') as f:
        f.write(text)

    print(f"Processed file {i+1}/{len(os.listdir(input_dir))}: {filename}")
