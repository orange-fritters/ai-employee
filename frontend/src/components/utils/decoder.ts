export const unicodeToChar = (text: string) => {
  return text
    .replace(/\\u[\dA-F]{4}/gi, function(match) {
      const char = String.fromCharCode(parseInt(match.replace(/\\u/g, ""), 16));
      return char;
    })
    .replace(/[\\s]/g, "")
    .slice(2, -2);
};

export const responseDecoder = (text: string) => {
  const pattern = /{(.*?)}/g;
};

export const convertToJSON = async (response: Response) => {
  const data = await response.json();
  const converted = JSON.parse(data);
  return converted;
};
