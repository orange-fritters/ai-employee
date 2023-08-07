import styled from "styled-components";

const Container = styled.div`
  width: 500px;
  height: 100vh;
`;

const Background = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;

  background-color: #d8d8d8;

  width: 100%;
  height: 100vh;

  ::-webkit-scrollbar {
    width: 10px;
    display: none;
  }
`;

const Window = styled.div`
  display: flex;
  flex-direction: column;
  background-color: white;

  width: 100%;
  height: 70vh;
  padding-top: 2.5vh;
  padding-bottom: 2.5vh;

  overflow-y: scroll;
  scroll-behavior: smooth;

  gap: 20px;
`;

export { Container, Background, Window };
