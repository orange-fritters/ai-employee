import React from "react";
import styled, { keyframes } from "styled-components";

interface IButton {
  type: "home" | "recommendation";
  loading: boolean;
}

const Button = ({ type, loading }: IButton) => {
  return (
    <StyledButton type={type} loading={loading}>
      {type === "home" ? "처음으로" : "서비스 더보기"}
    </StyledButton>
  );
};

export default Button;

const StyledButton = styled.button<{
  type: "home" | "recommendation";
  loading: boolean;
}>`
  position: relative;
  align-self: "flex-start";
  text-align: "center";
  background-color: #7478b0;
  color: white;
  border: 1px solid white;
  font-weight: 550;
  font-size: 16px;
  padding-top: 6.5px;
  padding-bottom: 6.5px;
  border-radius: 15px;
  box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.2);
  &:hover {
    background-color: #6d30d0;
    color: #fff;
    pointer: cursor;
  }
  width: -webkit-fill-available;
`;
