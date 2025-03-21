/**  MIT license https://opensource.org/licenses/MIT
”Copyright 2024-2025 Infosys Ltd.”
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/ 
import { ChangeDetectionStrategy, Component, OnInit } from '@angular/core';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';

import { Thread, ThreadState } from '../../../../../app/admin/metrics/metrics.model';

@Component({
  selector: 'jhi-thread-modal',
  templateUrl: './metrics-modal-threads.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class MetricsModalThreadsComponent implements OnInit {
  ThreadState = ThreadState;
  threadStateFilter?: ThreadState;
  threads?: Thread[];
  threadDumpAll = 0;
  threadDumpBlocked = 0;
  threadDumpRunnable = 0;
  threadDumpTimedWaiting = 0;
  threadDumpWaiting = 0;

  constructor(private activeModal: NgbActiveModal) {}

  ngOnInit(): void {
    this.threads?.forEach(thread => {
      if (thread.threadState === ThreadState.Runnable) {
        this.threadDumpRunnable += 1;
      } else if (thread.threadState === ThreadState.Waiting) {
        this.threadDumpWaiting += 1;
      } else if (thread.threadState === ThreadState.TimedWaiting) {
        this.threadDumpTimedWaiting += 1;
      } else if (thread.threadState === ThreadState.Blocked) {
        this.threadDumpBlocked += 1;
      }
    });

    this.threadDumpAll = this.threadDumpRunnable + this.threadDumpWaiting + this.threadDumpTimedWaiting + this.threadDumpBlocked;
  }

  getBadgeClass(threadState: ThreadState): string {
    if (threadState === ThreadState.Runnable) {
      return 'badge-success';
    } else if (threadState === ThreadState.Waiting) {
      return 'badge-info';
    } else if (threadState === ThreadState.TimedWaiting) {
      return 'badge-warning';
    } else if (threadState === ThreadState.Blocked) {
      return 'badge-danger';
    }
    return '';
  }

  getThreads(): Thread[] {
    return this.threads?.filter(thread => !this.threadStateFilter || thread.threadState === this.threadStateFilter) ?? [];
  }

  dismiss(): void {
    this.activeModal.dismiss();
  }
}
