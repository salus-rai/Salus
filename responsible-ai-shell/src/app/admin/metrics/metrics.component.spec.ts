/**
SPDX-License-Identifier: MIT
Copyright 2024 - 2025 Infosys Ltd.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/

import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { of } from 'rxjs';

import { MetricsComponent } from './metrics.component';
import { MetricsService } from './metrics.service';
import { Metrics } from './metrics.model';

describe('MetricsComponent', () => {
  let comp: MetricsComponent;
  let fixture: ComponentFixture<MetricsComponent>;
  let service: MetricsService;

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      declarations: [MetricsComponent],
    })
      .overrideTemplate(MetricsComponent, '')
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(MetricsComponent);
    comp = fixture.componentInstance;
    service = TestBed.inject(MetricsService);
  });

  describe('refresh', () => {
    it('should call refresh on init', () => {
      // GIVEN
      jest.spyOn(service, 'getMetrics').mockReturnValue(of({} as Metrics));

      // WHEN
      comp.ngOnInit();

      // THEN
      expect(service.getMetrics).toHaveBeenCalled();
    });
  });
});