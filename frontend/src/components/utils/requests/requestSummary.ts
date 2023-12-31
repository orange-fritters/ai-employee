import { unicodeToChar } from "../decoder";

/**
 *
 * @param title
 * @returns
 * @related
 * - get summary from preprocessed document
 *   - return io_model.get_summary(query.query)
 */
export const requestSummary = async (title: string) => {
  try {
    const response = await fetch("/api/summary", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ query: title }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    const unicodeString = JSON.stringify(data);
    const summary = unicodeToChar(unicodeString);

    return summary;
  } catch (error) {
    console.log(error);
  }
};
