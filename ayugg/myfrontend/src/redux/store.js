import { configureStore, createSlice } from '@reduxjs/toolkit';
import dataReducer from './dataSlice';

const rankingLine = createSlice({
  name: 'line',
  initialState : 'top',
  reducers:{
    changeLine(state, line){
      return state = line.payload;
    }
  }
});

const rankingTier= createSlice({
  name: 'tier',
  initialState : 'GOLD',
  reducers:{
    changeTier(state, tier){
      return state = tier.payload;
    }
  }
})

const rankingVersion= createSlice({
  name: 'version',
  initialState : '14.11.1',
  reducers:{
    changeVersion(state, ver){
      return state = ver.payload;
    }
  }
})

export const store = configureStore({
  reducer: {
    data: dataReducer,
    rankingLine: rankingLine.reducer,
    rankingTier: rankingTier.reducer,
    rankingVersion: rankingVersion.reducer,
  },
});

export let { changeLine } = rankingLine.actions
export let { changeTier } = rankingTier.actions
export let { changeVersion } = rankingVersion.actions