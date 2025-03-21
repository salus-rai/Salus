/**  MIT license https://opensource.org/licenses/MIT
”Copyright 2024-2025 Infosys Ltd.”
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/ 
import { Component, OnInit } from '@angular/core';
import { HttpErrorResponse } from '@angular/common/http';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';

import { HealthService } from './health.service';
import { Health, HealthDetails, HealthStatus } from './health.model';
import { HealthModalComponent } from './modal/health-modal.component';

@Component({
  selector: 'jhi-health',
  templateUrl: './health.component.html',
})
export class HealthComponent implements OnInit {
  health?: Health;

  constructor(private modalService: NgbModal, private healthService: HealthService) {}

  ngOnInit(): void {
    this.refresh();
  }

  getBadgeClass(statusState: HealthStatus): string {
    if (statusState === 'UP') {
      return 'badge-success';
    }
    return 'badge-danger';
  }

  refresh(): void {
    this.healthService.checkHealth().subscribe(
      health => (this.health = health),
      (error: HttpErrorResponse) => {
        if (error.status === 503) {
          this.health = error.error;
        }
      }
    );
  }

  showHealth(health: { key: string; value: HealthDetails }): void {
    const modalRef = this.modalService.open(HealthModalComponent);
    modalRef.componentInstance.health = health;
  }
}
