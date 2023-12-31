/**
 * This file contains the styled components for the search bar component.
 * It exports the following styled components:
 * - BackGround: a styled form element that serves as the background wrapper for the search bar
 * - SearchBarBox: a styled div element that wraps the search input and send button
 * - SearchInput: a styled input element that serves as the search bar input
 * - SmallSendButton: a styled button element that serves as the send button for the search bar
 *                    an image of a send icon is used as the button's background
 */
import styled from "styled-components";

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
  height: 20px;
  background-color: transparent;
  padding-left: 40px;
  &::placeholder {
    color: lightgray;
    font-size: 20px;
    line-height: 1;
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

export { BackGround, SearchBarBox, SearchInput, SmallSendButton };
