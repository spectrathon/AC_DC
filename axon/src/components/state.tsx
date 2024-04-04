import create from 'zustand';
import { GlobalGameState } from './types';

const useGameStore = create<GlobalGameState>((set) => ({
    playerLives: 5,
    playerScore: 0,
    decreasePlayerLives: () => set((state) => ({ playerLives: state.playerLives - 1 })),
    increasePlayerScore: (points) => set((state) => ({ playerScore: state.playerScore + points })),
}));

export default useGameStore;


