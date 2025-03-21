/**  MIT license https://opensource.org/licenses/MIT
”Copyright 2024-2025 Infosys Ltd.”
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/ 
import { Component, Input } from '@angular/core';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';

import { Thread, ThreadState } from '../../../../../app/admin/metrics/metrics.model';
import { MetricsModalThreadsComponent } from '../metrics-modal-threads/metrics-modal-threads.component';

@Component({
  selector: 'jhi-jvm-threads',
  templateUrl: './jvm-threads.component.html',
})
export class JvmThreadsComponent {
  threadStats = {
    threadDumpAll: 0,
    threadDumpRunnable: 0,
    threadDumpTimedWaiting: 0,
    threadDumpWaiting: 0,
    threadDumpBlocked: 0,
  };

  @Input()
  set threads(threads: Thread[] | undefined) {
    this._threads = threads;

    threads?.forEach(thread => {
      if (thread.threadState === ThreadState.Runnable) {
        this.threadStats.threadDumpRunnable += 1;
      } else if (thread.threadState === ThreadState.Waiting) {
        this.threadStats.threadDumpWaiting += 1;
      } else if (thread.threadState === ThreadState.TimedWaiting) {
        this.threadStats.threadDumpTimedWaiting += 1;
      } else if (thread.threadState === ThreadState.Blocked) {
        this.threadStats.threadDumpBlocked += 1;
      }
    });

    this.threadStats.threadDumpAll =
      this.threadStats.threadDumpRunnable +
      this.threadStats.threadDumpWaiting +
      this.threadStats.threadDumpTimedWaiting +
      this.threadStats.threadDumpBlocked;
  }

  get threads(): Thread[] | undefined {
    return this._threads;
  }

  private _threads: Thread[] | undefined;

  constructor(private modalService: NgbModal) {}

  open(): void {
    const modalRef = this.modalService.open(MetricsModalThreadsComponent);
    modalRef.componentInstance.threads = this.threads;
  }
}
