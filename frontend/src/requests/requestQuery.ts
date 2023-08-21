/**
 *
 * @param {string} input The user's input.
 * @param {string} title title of the article.
 * @returns {Promise<Response>} - The response object from the backend.
 * @description
 * The basic form of the request to the backend asking for an answer to the user's input.
 *
 * @related
 * - get_answer_from_document(document: str, query: str):
 * - async def get_chat_response(query: Query):
 */
export const requestQuery = async (
  input: string,
  title: string
): Promise<Response> => {
  const response = await fetch("/api/query", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ query: input, title: title }),
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  return response;
};
