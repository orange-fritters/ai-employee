import { configureStore } from "@reduxjs/toolkit";
import messageReducer from "./message.slice";
import recommendationSlicer from "./recommendation.slice";
import multiturnSlice from "./multiturn.slice";

const store = configureStore({
  reducer: {
    chat: messageReducer,
    multiturn: multiturnSlice,
    recommendation: recommendationSlicer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export default store;
