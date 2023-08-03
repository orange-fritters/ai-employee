import { selectRecTitles, selectUserMessages } from "../../../redux/selectors";
import { useSelector } from "react-redux";

export const requestMultiturn = async (input: string) => {
  const titles = useSelector(selectRecTitles);
  const userMessages = useSelector(selectUserMessages);

  const response = await fetch("/api/multi-turn/initial", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      input: input,
      titles: titles,
      context: userMessages,
    }),
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  return response;
};
