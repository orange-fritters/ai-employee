import { createSlice, PayloadAction } from "@reduxjs/toolkit";

interface IRecState {
  now: "home" | "asking" | "recommendation" | "multiturn" | "search";
}
export interface IRecElement {
  rank: number;
  title: string;
}

const RecList: IRecElement[] = [];
const RecState: IRecState = {
  now: "search",
};

export const recommendationSlice = createSlice({
  name: "recommendation",
  initialState: {
    recommendations: RecList,
    now: RecState,
  },
  reducers: {
    /** Store received recommendation arrays */
    updateRecommendation: (
      state,
      action: PayloadAction<{
        recommendationResponse: IRecElement[];
      }>
    ) => {
      state.recommendations = action.payload.recommendationResponse;
    },

    /** Update state */
    updateRecommendationState: (
      state,
      action: PayloadAction<{
        recommendationState: IRecState;
      }>
    ) => {
      state.now = action.payload.recommendationState;
    },

    /** Swap rank of two items, especially, clicked one */
    swapRank: (
      state,
      action: PayloadAction<{
        titleClicked: string;
      }>
    ) => {
      const { titleClicked } = action.payload;

      if (!titleClicked) {
        return;
      }

      const currFirstItem = state.recommendations.find(
        (elem) => elem.rank === 1
      );
      const clickedItem = state.recommendations.find(
        (elem) => elem.title === titleClicked
      );

      if (!currFirstItem || !clickedItem) {
        return;
      }

      const rankCandidate = clickedItem.rank;

      currFirstItem.rank = rankCandidate;
      clickedItem.rank = 1;

      state.recommendations.sort((a, b) => a.rank - b.rank);
    },
  },
});

export const {
  updateRecommendation,
  updateRecommendationState,
  swapRank,
} = recommendationSlice.actions;
export default recommendationSlice.reducer;
