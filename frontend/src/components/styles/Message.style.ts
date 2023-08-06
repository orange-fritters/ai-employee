import styled, { keyframes } from "styled-components";
import { IMessage } from "../Message";

const TimeBox = styled.div`
  display: grid;

  justify-self: center;
  justify-content: center;
  align-items: center;
  align-self: center;

  height: 25px;
  width: 30%;
  margin-bottom: 10px;
  font-family: "Noto Sans KR", sans-serif;
  font-weight: 600;

  border-radius: 15px;
  background-color: white;
  box-shadow: 0 0 5px 2.5px rgba(0, 0, 0, 0.1);
`;

const MessageBox = styled.div<{
  sender: "user" | "bot";
  type: IMessage["type"];
}>`
  display: grid;
  grid-column: 1 / 3;
  position: relative;
  text-align: ${(props: { sender: string; }) => (props.sender === "bot" ? "left" : "right")};
  background-color: ${(props : { sender : string}) =>
    props.sender === "bot" ? "#eeeeee" : "#0084ff"};
  color: ${(props : { sender : string}) => (props.sender === "bot" ? "#000" : "#fff")};
  padding: 20px;
  border-radius: ${(props : { sender : string}) =>
    props.sender === "bot" ? "0px 30px 30px 30px" : "30px 0px 30px 30px"};
  box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.2);
`;

const LoadingBox = styled.div`
  display: flex;
  position: relative;
  justify-content: center;
  align-items: center;
  background-color: #eeeeee;
  color: #000;
  padding: 20px;
  border-radius: 0px 30px 30px 30px;
  box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.2);
  width: 100%;
`;

const slideInFromLeft = keyframes`
  0% {
    transform: translateX(-100%);
  }
  100% {
    transform: translateX(0);
  }
`;

const ButtonBox = styled.div<{
  type: IMessage["type"];
  loading: boolean;
}>`
  grid-column: 1 / 3;
  display: grid;
  grid-template-columns: 1fr 1fr;
  justify-items: center;
  position: relative;
  align-self: "flex-start";
  text-align: "left";
  background-color: #648fd9;
  color: "#000";
  max-width: ${(props : { type : string}) => (props.type === "default" ? "60%" : "100%")};
  margin-left: ${(props : { type : string}) => (props.type === "default" ? "25px" : "0px")};
  margin-right: 0px;
  padding: 5px;
  border-radius: 5px 17px 17px 17px;
  box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.2);

  height: ${(props : { loading : boolean }) => (props.loading ? "0px" : "50px")};
  transition: height 1s ease-in-out;
  animation: ${slideInFromLeft} 1s ease-out;

  column-gap: 10px;
  padding: 10px;
`;

const InitButtonBox = styled(ButtonBox)`
  grid-template-columns: 1fr 1fr;
`;

const SearchButtonBox = styled(ButtonBox)`
  grid-template-columns: 1fr;
`;

const SingleResponse = styled.div<{
  type: IMessage["type"];
  sender: "user" | "bot";
}>`
  display: grid;
  max-width: 60%;
  grid-template-columns: ${(props : { type : string}) =>
    props.type === "default" ? "1fr" : "1fr 1fr"};
  margin-left: ${(props : { sender : string}) => (props.sender === "bot" ? "25px" : "0px")};
  margin-right: ${(props : { sender : string}) => (props.sender === "bot" ? "0px" : "25px")};
  align-self: ${(props : { sender : string}) =>
    props.sender === "bot" ? "flex-start" : "flex-end"};
  grid-template-rows: auto;
  grid-column-gap: 12px;
  grid-row-gap: 15px;
  margin-left: 25px;
`;

const RecResponse = styled.div`
  display: grid;
  // grid-template-rows: 1fr 1fr 1fr 1fr;
  grid-template-rows: 1fr 1fr;
  width: 55%;
  margin-left: 25px;
  margin-right: 0px;
  align-self: flex-start;
  grid-row-gap: 12px;
  padding: 2.5%;

  justify-items: center;
  position: relative;
  background-color: rgb(100, 143, 217);
  border-radius: 5px 17px 17px;
  box-shadow: rgba(0, 0, 0, 0.2) 0px 2px 4px;
  transition: height 1s ease-in-out 0s;
  animation: 1s ease-out 0s 1 normal none running bxdTFl;
`;

const Recommendation = styled.button`
  position: relative;
  align-self: "flex-start";
  text-align: "center";
  background-color: #6e9ef0;
  color: white;
  border: none;
  font-weight: 550;
  font-size: 16px;
  padding-top: 6.5px;
  padding-bottom: 6.5px;
  border-radius: 5px;
  box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.2);
  &:hover {
    background-color: #2162d1;
    color: rgb(255, 255, 255);
    cursor: pointer;
    box-shadow: rgba(0, 0, 0, 0.35) 0px 2px 4px;
    font-weight: 600;
  }
  width: 100%;
`;

const popIn = keyframes`
  0% {
    transform: scale(0);
    opacity: 0;
  }
  80% {
    transform: scale(1.1);
    opacity: 1;
  }
  100% {
    transform: scale(1);
  }
`;

const FloatingButton = styled.button`
  position: absolute;
  top: 0px;
  right: -50px;
  box-shadow: 0px 1.5px 3px rgba(0, 0, 0, 0.16),
    0px 1.5px 3px rgba(0, 0, 0, 0.23);
  background: #6a5acd;
  color: #fff;
  border: none;
  border-radius: 50%;
  width: 45px;
  height: 45px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  font-weight: 700;

  &:hover {
    background: #0073e6;
  }

  animation: ${popIn} 0.5s ease;
  animation-delay: 1s;
  animation-fill-mode: backwards;
`;

export { TimeBox, MessageBox, LoadingBox, ButtonBox, SingleResponse, RecResponse, Recommendation, FloatingButton, InitButtonBox, SearchButtonBox };