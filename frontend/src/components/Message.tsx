import styled from "styled-components";

export interface IMessage {
  sender: "user" | "bot";
  text: string;
}

export const Message = styled.div<{ sender: "user" | "bot" }>`
  position: relative;
  align-self: ${(props) =>
    props.sender === "bot" ? "flex-start" : "flex-end"};
  background-color: ${(props) =>
    props.sender === "bot" ? "#eeeeee" : "#0084ff"};
  color: ${(props) => (props.sender === "bot" ? "#000" : "#fff")};

  margin-left: 25px;
  padding: 20px;
  border-radius: 0px 30px 30px 30px;
  width: 60%;
`;
