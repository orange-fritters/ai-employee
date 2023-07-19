import { useDispatch } from "react-redux";
import { handleStream } from "../../redux/message.slice";

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
