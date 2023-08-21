/**
 * @param text {string} - The text to be decoded.
 * @returns {string} - The decoded text.
 * @description
 * This function decodes the unicode characters in the response object from the backend.
 */
export const unicodeToChar = (text: string): string => {
  return text
    .replace(/\\u[\dA-F]{4}/gi, function(match) {
      const char = String.fromCharCode(parseInt(match.replace(/\\u/g, ""), 16));
      return char;
    })
    .replace(/[\\s]/g, "")
    .slice(2, -2);
};

/**
 * @param {Response} response - The text to be decoded.
 * @returns { Promise<any> }
 * @description
 * This function decodes the response object from the backend as json object.
 */
export const convertToJSON = async (response: Response): Promise<any> => {
  const data = await response.json();
  const converted = JSON.parse(data);
  return converted;
};
