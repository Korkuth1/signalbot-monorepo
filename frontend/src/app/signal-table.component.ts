import { Component, effect } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SignalService } from './services/signal.service';

@Component({
  selector: 'app-signal-table',
  standalone: true,
  imports: [CommonModule],
  providers: [SignalService],
  template: `
<h2 class="text-xl font-bold mb-4">📈 Aktuelle Signale</h2>
<table class="table-auto w-full border border-gray-300 text-sm">
  <thead>
    <tr>
      <th class="border p-2">Symbol</th>
      <th class="border p-2">Empfehlung</th>
      <th class="border p-2">RSI</th>
      <th class="border p-2">MACD</th>
      <th class="border p-2">Signal</th>
      <th class="border p-2">VWAP</th>
      <th class="border p-2">EMA50</th>
      <th class="border p-2">EMA200</th>
      <th class="border p-2">High</th>
      <th class="border p-2">Low</th>
      <th class="border p-2">Volumen</th>
      <th class="border p-2">BB Upper</th>
      <th class="border p-2">BB Lower</th>
      <th class="border p-2">Zeit</th>
    </tr>
  </thead>
  <tbody>
    <tr *ngFor="let s of signalService.signals()">
      <td class="border p-2">{{ s.symbol }}</td>
      <td class="border p-2">{{ s.recommendation }}</td>
      <td class="border p-2">{{ s.rsi?.toFixed(2) ?? '-' }}</td>
      <td class="border p-2">{{ s.macd?.toFixed(4) ?? '-' }}</td>
      <td class="border p-2">{{ s.signal_line?.toFixed(4) ?? '-' }}</td>
      <td class="border p-2">{{ s.vwap?.toFixed(2) ?? '-' }}</td>
      <td class="border p-2">{{ s.ema50?.toFixed(2) ?? '-' }}</td>
      <td class="border p-2">{{ s.ema200?.toFixed(2) ?? '-' }}</td>
      <td class="border p-2">{{ s.high?.toFixed(2) ?? '-' }}</td>
      <td class="border p-2">{{ s.low?.toFixed(2) ?? '-' }}</td>
      <td class="border p-2">{{ s.volume ?? '-' }}</td>
      <td class="border p-2">{{ s.bb_upper?.toFixed(2) ?? '-' }}</td>
      <td class="border p-2">{{ s.bb_lower?.toFixed(2) ?? '-' }}</td>
      <td class="border p-2">{{ s.timestamp | date:'short' }}</td>
    </tr>
  </tbody>
</table>

  `
})
export class SignalTableComponent {
  constructor(public signalService: SignalService) {}
}
