import React from "react";
import { useDispatch } from "react-redux";

import {
  handleRecommendationButton,
  handleSearchButton,
} from "../utils/handleButton";
import * as S from "./styles/Button.style";

export interface IButton {
  type: "search" | "recommendation" ;
  loading?: boolean;
  text?: string;
}

/**
 * A button component that can be used to trigger different actions based on its type.
 * @param type The type of the button. Can be "home", "recommendation", "multiturn", or "search".
 * @returns A button element that triggers the appropriate action when clicked.
 */
const Button = ({ type }: IButton) => {
  const dispatch = useDispatch();

  const handleClick = async () => {
    switch (type) {
      case "search":
        handleSearchButton(dispatch);
        break;
      case "recommendation":
        handleRecommendationButton(dispatch);
        break;
      default:
        break;
    }
  };

  /**
   * @returns The text to display on the button.
   */
  const getText = () => {
    const textByType = {
      recommendation: "추천",
      search: "처음으로",
    };
    return textByType[type] || "";
  };

  return <S.StyledButton onClick={handleClick}>{getText()}</S.StyledButton>;
};

export default Button;
