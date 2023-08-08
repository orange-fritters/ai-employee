import React from "react";
import * as S from "./styles/Header.style";

/**
 * Renders the header component with the title "AI 사원".
 * @returns TSX element
 */
const Header = () => {
  return (
    <S.HeaderBox>
      <S.HeaderText>AI 사원</S.HeaderText>
    </S.HeaderBox>
  );
};

export default Header;
