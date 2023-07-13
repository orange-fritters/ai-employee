import styled from "styled-components";

export interface IMessage {
  sender: "user" | "bot";
  text: string;
}

export const Message = styled.div<{ sender: "user" | "bot" }>`
  position: relative;
  align-self: ${(props) =>
    props.sender === "bot" ? "flex-start" : "flex-end"};
  text-align: ${(props) => (props.sender === "bot" ? "left" : "right")};
  background-color: ${(props) =>
    props.sender === "bot" ? "#eeeeee" : "#0084ff"};
  color: ${(props) => (props.sender === "bot" ? "#000" : "#fff")};

  margin-left: ${(props) => (props.sender === "bot" ? "25px" : "0px")};
  margin-right: ${(props) => (props.sender === "bot" ? "0px" : "25px")};
  padding: 20px;
  border-radius: ${(props) =>
    props.sender === "bot" ? "0px 30px 30px 30px" : "30px 0px 30px 30px"};
  max-width: 60%;
`;
