import { configureStore } from "@reduxjs/toolkit";
import messageReducer from "./message.slice";
import recommendationSlicer from "./recommendation.slicer";

const store = configureStore({
  reducer: {
    chat: messageReducer,
    recommendation: recommendationSlicer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export default store;
