import { IMessage } from "../components/Message";

/**
 * @description
 * Default guide message to be shown when the user first enters the chatbot
 * Two options are available: @Search and @Multiturn
 */
export const dMessages: IMessage[] = [
  {
    sender: "bot",
    text: "",
    type: "time",
    loading: false,
  },
  {
    sender: "bot",
    text:
      "안녕하세요!\n저는 여러분의 복지 서비스를 도와드릴 AI 봇입니다. 원하시는 서비스를 선택해주세요.",
    type: "initial",
    loading: false,
  },
];

/**
 * @description
 * Default guide message to be shown when the user click @Search
 */
export const dSearch: IMessage[] = [
  {
    sender: "bot",
    text: "",
    type: "time",
    loading: false,
  },
  {
    sender: "bot",
    text:
      "복지 서비스에 대한 정보를 찾아드려요!\n원하시는 서비스에 대해 무엇이든 물어보세요.",
    type: "default",
    loading: false,
  },
];

/**
 * @description
 * Default guide message to be shown when the user click @Multiturn
 */
export const dMultiturn: IMessage[] = [
  {
    sender: "bot",
    text:
      "당신의 상황에 알맞은 복지 서비스를 찾아줄게요!\n\nEX. 취직 준비에 도움을 받고 싶어요.",
    type: "default",
    loading: false,
  },
];
