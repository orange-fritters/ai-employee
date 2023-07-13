import React, { useEffect, useState } from "react";
import styled from "styled-components";
import axios from "axios";

interface ISearchBarProps {
  handleMessages: (query: string, who: "bot" | "user") => void;
}

const SearchBar: React.FC<ISearchBarProps> = ({ handleMessages }) => {
  const PUBLIC_URL = process.env.PUBLIC_URL;
  const sendButton = `${PUBLIC_URL}/icon.svg`;

  const [input, setInput] = useState<string>("");
  const [query, setQuery] = useState<string>("");

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setInput(event.target.value);
    setQuery(event.target.value);
  };

  const makeQuery = async () => {
    try {
      handleMessages(input, "user");
      setInput("");
      const res = await axios.post("/query", { query: query });
      handleMessages(res.data.response, "bot");
      setQuery("");
    } catch (error) {
      console.error("Error:", error);
    }
  };

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    makeQuery();
  };

  return (
    <BackGround onSubmit={handleSubmit}>
      <SearchBarBox>
        <SearchInput
          placeholder="   질문을 입력해주세요."
          type="text"
          value={input}
          onChange={handleInputChange}
        />
        <SmallSendButton type="submit">
          <img src={sendButton} />
        </SmallSendButton>
      </SearchBarBox>
    </BackGround>
  );
};

export default SearchBar;

const BackGround = styled.form`
  background-color: white;
  width: 100%;
  height: 15vh;

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
  font-size: 16px;
  background-color: transparent;
  padding-left: 40px;
  &::placeholder {
    color: lightgray;
    font-size: 20px; /* Adjust the font size as needed */
    line-height: 1; /* Ensures vertical centering */
  }
`;

const SmallSendButton = styled.button`
  background-color: transparent;
  border: none;

  img {
    width: 50px;
    height: 50px;
    background-size: cover;
    cursor: pointer;
    border: none;
    margin-right: 10px;
  }
`;
