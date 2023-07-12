import React, { useState } from "react";
import styled from "styled-components";

const BackGround = styled.div`
  background-color: white;
  width: 35%;
  height: 15vh;

  padding-top: 10px;
  padding-bottom: 10px;

  display: flex;
  align-items: center;
  justify-content: center;
`;

const SearchBarBox = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;

  background-color: white;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);

  width: 80%;
  height: 90%;

  border-radius: 25px;

  color: black;
`;

const SearchInput = styled.input`
  flex: 1;
  border: none;
  outline: none;
  padding: 10px;
  font-size: 16px;
  background-color: transparent;
  &::placeholder {
    color: lightgray;
    font-size: 20px; /* Adjust the font size as needed */
    line-height: 1; /* Ensures vertical centering */
  }
`;

const SmallSendButton = styled.img`
  width: 50px;
  height: 50px;
  background-size: cover;
  cursor: pointer;
  border: none;
  margin-right: 10px;
`;

interface ISearchBarProps {
  onSearch: (query: string) => void;
}

const SearchBar: React.FC<ISearchBarProps> = ({ onSearch }) => {
  const PUBLIC_URL = process.env.PUBLIC_URL;
  const sendButton = `${PUBLIC_URL}/icon.svg`;

  const [input, setInput] = useState<string>("");

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    console.log(event.target.value);
    setInput(event.target.value);
  };

  const handleButtonClick = () => {
    onSearch(input);
    setInput("");
  };

  return (
    <BackGround>
      <SearchBarBox>
        <SearchInput
          placeholder="   질문을 입력해주세요."
          value={input}
          onChange={handleInputChange}
          onKeyDown={(e: React.KeyboardEvent<HTMLInputElement>) => {
            if (e.key === "Enter") {
              handleButtonClick();
            }
          }}
        />
        <SmallSendButton src={sendButton} onClick={handleButtonClick} />
      </SearchBarBox>
    </BackGround>
  );
};

export default SearchBar;
