/**  MIT license https://opensource.org/licenses/MIT
”Copyright 2024-2025 Infosys Ltd.”
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/ 
import { Component, OnDestroy, OnInit } from '@angular/core';

import { AlertService, Alert } from '../../../app/core/util/alert.service';

@Component({
  selector: 'jhi-alert',
  templateUrl: './alert.component.html',
})
export class AlertComponent implements OnInit, OnDestroy {
  alerts: Alert[] = [];

  constructor(private alertService: AlertService) {}

  ngOnInit(): void {
    this.alerts = this.alertService.get();
  }

  setClasses(alert: Alert): { [key: string]: boolean } {
    const classes = { 'jhi-toast': Boolean(alert.toast) };
    if (alert.position) {
      return { ...classes, [alert.position]: true };
    }
    return classes;
  }

  ngOnDestroy(): void {
    this.alertService.clear();
  }

  close(alert: Alert): void {
    alert.close?.(this.alerts);
  }
}
