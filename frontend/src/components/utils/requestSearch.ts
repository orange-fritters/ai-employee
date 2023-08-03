import { IRecElement } from "../../redux/recommendation.slice";

export const requestSearch = async (input: string, titles: IRecElement[]) => {
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
