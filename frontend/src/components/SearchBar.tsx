import React, { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { RootState } from "../redux/store";

import * as S from "./styles/styles";
import {
  selectFirstRecommendation,
} from "../redux/selectors";
import { handleSubmitWhenAsking, handleSubmitWhenDefault, handleSubmitWhenHome, handleSubmitWhenMultiturn, handleSubmitWhenSearch } from "./utils/handleSubmit";

const SearchBar: React.FC = () => {
  const dispatch = useDispatch();
  const [input, setInput] = useState<string>("");
  const state = useSelector((state: RootState) => state.recommendation.now);
  const rec = useSelector(selectFirstRecommendation);
  const sendButton = `${process.env.PUBLIC_URL}/icon.svg`;

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    switch (state.now) {
      case "home":
        handleSubmitWhenHome(input, setInput, dispatch);
        break;
      case "search":
        handleSubmitWhenSearch(input, setInput, dispatch);
        break;
      case "asking":
        handleSubmitWhenAsking(input, rec, setInput, dispatch);
        break;
      case "multiturn":
        handleSubmitWhenMultiturn(input, setInput, dispatch);
        break;
      default:
        handleSubmitWhenDefault(setInput, dispatch);
    }
  };

  return (
    <S.BackGround onSubmit={handleSubmit}>
      <S.SearchBarBox>
        <S.SearchInput
          placeholder="   질문을 입력해주세요."
          type="text"
          value={input}
          onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
            setInput(e.target.value)
          }
        />
        <S.SmallSendButton type="submit">
          <img src={sendButton} />
        </S.SmallSendButton>
      </S.SearchBarBox>
    </S.BackGround>
  );
};

export default SearchBar;
