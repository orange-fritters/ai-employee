import React from "react";
import { useDispatch, useSelector } from "react-redux";

import { RootState } from "../redux/store";
import {
  handleHomeButton,
  handleMultiturnButton,
  handleRecommendationButton,
  handleSearchButton,
} from "./utils/handleButton";
import * as S from "./styles/Button.style";

export interface IButton {
  type: "home" | "recommendation" | "multiturn" | "search";
  loading?: boolean;
  text?: string;
}

/**
 * A button component that can be used to trigger different actions based on its type.
 * @param type - The type of the button. Can be "home", "recommendation", "multiturn", or "search".
 * @returns A button element that triggers the appropriate action when clicked.
 */
const Button = ({ type }: IButton) => {
  const dispatch = useDispatch();
  const recommendations = useSelector(
    (state: RootState) => state.recommendation.recommendations
  );

  const handleClick = async () => {
    switch (type) {
      case "home":
        handleHomeButton(dispatch);
        break;
      case "search":
        handleSearchButton(dispatch);
        break;
      case "recommendation":
        handleRecommendationButton(recommendations, dispatch);
        break;
      case "multiturn":
        handleMultiturnButton(dispatch);
        break;
    }
  };

  /**
   * @returns The text to display on the button.
   */
  const getText = () => {
    const textByType = {
      home: "처음",
      recommendation: "추천",
      multiturn: "추천받기",
      search: "문의하기",
    };
    return textByType[type] || "";
  };

  return <S.StyledButton onClick={handleClick}>{getText()}</S.StyledButton>;
};

export default Button;
