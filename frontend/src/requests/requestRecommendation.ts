/**
 * @param  {string} input The input text to be sent to the backend.
 * @returns {Promise<Response>} - The response object from the backend.
 * @related
 * - [prompt for the original](../../../../../server/model/utils/convert_prompt.py)
 *   - get_answer_from_document(document: str, query: str):
 *   - def get_topN_title(self, query, n=5):
 */
export const requestRecommendation = async (
  input: string
): Promise<Response> => {
  const response = await fetch("/api/recommendation", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ query: input }),
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  return response;
};
