import React from "react";
import styled from "styled-components";

const Header = () => {
  return (
    <HeaderBox>
      <HeaderText>AI 사원</HeaderText>
    </HeaderBox>
  );
};

const HeaderBox = styled.div`
  background-color: white;
  border-bottom: 1px solid #ccc;
  box-shadow: 0px 30px 0px 0px rgba(0, 0, 0, 30);

  width: 100%;
  height: 10vh;

  display: flex;
  align-items: center;
  vertical-align: middle;
`;

const HeaderText = styled.div`
  padding-left: 40px;
  font-family: "Noto Sans KR", sans-serif;
  font-weight: 900;
  font-size: 25px;

  color: #2979ff;
`;
export default Header;
