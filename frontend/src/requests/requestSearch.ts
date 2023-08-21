import { IRecElement } from "../redux/recommendation.slice";

/**
 * @param  {string} input The input text to be sent to the backend.
 * @returns {Promise<Response>} - The response object from the backend.
 * @related
 * - [prompt for the original](../../../../../server/model/utils/convert_prompt.py)
 *   - async def get_search(search: Search):
 *   - async def get_chat_response(query: Query):
 */
export const requestSearch = async (
  input: string,
  titles: IRecElement[]
): Promise<Response> => {
  const response = await fetch("/api/search", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ query: input, titles: titles }),
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  return response;
};
