export const unicodeToChar = (text: string) => {
  return text.replace(/\\u[\dA-F]{4}/gi, function(match) {
    return String.fromCharCode(parseInt(match.replace(/\\u/g, ""), 16));
  });
};

export const responseDecoder = (text: string) => {
  const pattern = /{(.*?)}/g;
};
