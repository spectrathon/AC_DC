interface GameState {
    playerLives: number;
    playerScore: number;
    // Add other game state properties here
}

interface GameActions {
    decreasePlayerLives: () => void;
    increasePlayerScore: (points: number) => void;
    // Add other game actions here
}

export type GlobalGameState = GameState & GameActions