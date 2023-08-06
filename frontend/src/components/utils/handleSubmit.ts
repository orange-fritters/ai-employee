import React, { useState } from "react";
import { useDispatch } from "react-redux";

import { getRecommendation, getRetrieval } from "./handleRecommendation";
import { pushResponse } from "../../redux/message.slice";
import { IRecElement, updateRecommendation, updateRecommendationState } from "../../redux/recommendation.slice";
import { requestSearch } from "./requests/requestSearch";
import { streamResponse } from "./requests/streamResponse";
import { requestQuery } from "./requests/requestQuery";
import { dMessages } from "../../redux/defaultMessages";
import { handleMultiturn } from "./handleMultiturn";

const handleSubmitWhenHome = async (
    input: string,
    setInput: React.Dispatch<React.SetStateAction<string>>,
    dispatch: ReturnType<typeof useDispatch>
  ) => {
    getRecommendation(input, dispatch);
    dispatch(pushResponse({ text: input, sender: "user", loading: false }));
    setInput("");
    dispatch(
    pushResponse({
        text: "",
        sender: "bot",
        loading: true,
        type: "default",
      })
    );
    dispatch(
      updateRecommendationState({ recommendationState: { now: "asking" } })
    );
}

const handleSubmitWhenSearch = async (
    input: string,
    setInput: React.Dispatch<React.SetStateAction<string>>,
    dispatch: ReturnType<typeof useDispatch>
) => {
    const query = input;
    setInput("");
    dispatch(pushResponse({ text: query, sender: "user", loading: false }));
    dispatch(
      pushResponse({
        text: "",
        sender: "bot",
        loading: true,
        type: "default",
      })
    );
    const titles = await getRetrieval(query, dispatch);
    try {
      await new Promise((resolve) => setTimeout(resolve, 1000));
      const response = await requestSearch(input, titles);
      if (response.body) {
        dispatch(pushResponse({ text: "", sender: "bot", loading: false }));
        const reader = response.body.getReader();
        const decoder = new TextDecoder("utf-8");
        await streamResponse(dispatch, reader, decoder);
      }
    } catch (error) {
      dispatch(
        pushResponse({
          text: "오류가 발생하였습니다. 처음으로 돌아갑니다.",
          sender: "bot",
          loading: false,
        })
      );
    }
    dispatch(
      updateRecommendationState({ recommendationState: { now: "asking" } })
    );
}

const handleSubmitWhenAsking = async (
    input: string,
    rec: IRecElement,
    setInput: React.Dispatch<React.SetStateAction<string>>,
    dispatch: ReturnType<typeof useDispatch>,
) => {
    try {
        dispatch(
          pushResponse({ text: input, sender: "user", loading: false })
        );
        setInput("");
        if (rec !== undefined && rec !== null) {
          await new Promise((resolve) => setTimeout(resolve, 1000));
          const response = await requestQuery(input, rec.title);
          if (response.body) {
            const reader = response.body.getReader();
            const decoder = new TextDecoder("utf-8");
            await streamResponse(dispatch, reader, decoder);
          }
        } else {
          dispatch(
            pushResponse({
              text: "오류가 발생하였습니다. 처음으로 돌아갑니다.",
              sender: "bot",
              loading: false,
            })
          );
          dispatch(
            updateRecommendationState({
              recommendationState: { now: "home" },
            })
          );
          dispatch(pushResponse({ ...dMessages[0] }));
          dispatch(pushResponse({ ...dMessages[1] }));
          dispatch(updateRecommendation({ recommendationResponse: [] }));
        }
    } catch (error) {
        console.error("Error:", error);
    }
}

const handleSubmitWhenMultiturn = async (
    input: string,
    setInput: React.Dispatch<React.SetStateAction<string>>,
    dispatch: ReturnType<typeof useDispatch>,
) =>{
    const question = input;
    setInput("");
    handleMultiturn(question, dispatch);
    dispatch(
      pushResponse({ text: question, sender: "user", loading: false })
    );
    dispatch(
      pushResponse({
        text: "",
        sender: "bot",
        loading: true,
        type: "default",
      })
    );
}

const handleSubmitWhenDefault = async (
    setInput: React.Dispatch<React.SetStateAction<string>>,
    dispatch: ReturnType<typeof useDispatch>,
) => {
    setInput("");
    dispatch(
        pushResponse({
          text: "새로고침해주세요.",
          sender: "bot",
          loading: false,
        })
    );
};


export { handleSubmitWhenHome, handleSubmitWhenSearch, handleSubmitWhenAsking, handleSubmitWhenMultiturn, handleSubmitWhenDefault} 