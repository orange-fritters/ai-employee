import { useDispatch } from "react-redux";
import { handleStream } from "../redux/message.slice";

/**
 * @param dispatch useDispatch from react-redux.
 * @param reader stream reader.
 * @param decoder stream decoder.
 * @description
 * This function is used to stream the response from the openai api
 * Request parameter stream set to true, and the response is streamed
 * Need while and reader, decoder to read the response.
 * Then, handleStream attaches the word to the redux store.
 */
export const streamResponse = async (
  dispatch: ReturnType<typeof useDispatch>,
  reader: ReadableStreamDefaultReader<Uint8Array>,
  decoder: TextDecoder
) => {
  while (true) {
    const { value, done } = await reader.read();
    if (done) {
      dispatch(handleStream({ text: " ", loading: false }));
      break;
    }
    const text = decoder.decode(value);
    dispatch(handleStream({ text: text, loading: true }));
  }
};
