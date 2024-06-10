export interface Prediction {
  date: string;
  power: number;
}

export interface PredictionHistory {
  date: string;
  real: number;
  prediction: number;
}
