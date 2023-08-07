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
  loading: boolean;
  text?: string;
}

const Button = ({ type, loading }: IButton) => {
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

  const getText = () => {
    const textByType = {
      home: "처음",
      recommendation: "추천",
      multiturn: "추천받기",
      search: "문의하기",
    };
    return textByType[type] || "";
  };

  return (
    <S.StyledButton onClick={handleClick} type={type} loading={loading}>
      {getText()}
    </S.StyledButton>
  );
};

export default Button;
