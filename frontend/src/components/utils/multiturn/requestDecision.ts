import {
  selectRecTitles,
  selectRecommendations,
  selectUserMessages,
} from "../../../redux/selectors";
import { useSelector } from "react-redux";

export const requestDecision = async (input: string) => {
  const titles = useSelector(selectRecommendations);

  const response = await fetch("/api/multi-turn/decide-sufficiency", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      input: input,
      titles: titles,
    }),
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  return response;
};
