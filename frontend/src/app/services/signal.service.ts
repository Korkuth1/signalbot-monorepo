import { inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { signal, effect } from '@angular/core';

export interface SignalData {
  symbol: string;
  recommendation: string;
  rsi: number;
  macd: number;
  signal_line: number;
  timestamp: string;
  vwap: number;
  ema50: number;
  ema200: number;
  high: number;
  low: number;
  volume: number;
  bb_upper: number;
  bb_lower: number;
}

export class SignalService {
  private http = inject(HttpClient);

  signals = signal<SignalData[]>([]);

  constructor() {
    this.loadSignals();
  }

  loadSignals() {
    this.http.get<SignalData[]>('http://localhost:5000/api/signals').subscribe(data => {
      this.signals.set(data);
    });
  }
}
