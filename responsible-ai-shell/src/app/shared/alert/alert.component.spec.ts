/**  MIT license https://opensource.org/licenses/MIT
”Copyright 2024-2025 Infosys Ltd.”
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/ 
jest.mock('app/core/util/alert.service');

import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';

import { AlertService } from 'app/core/util/alert.service';

import { AlertComponent } from './alert.component';

describe('Alert Component', () => {
  let comp: AlertComponent;
  let fixture: ComponentFixture<AlertComponent>;
  let mockAlertService: AlertService;

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      declarations: [AlertComponent],
      providers: [AlertService],
    })
      .overrideTemplate(AlertComponent, '')
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AlertComponent);
    comp = fixture.componentInstance;
    mockAlertService = TestBed.inject(AlertService);
  });

  it('Should call alertService.get on init', () => {
    // WHEN
    comp.ngOnInit();

    // THEN
    expect(mockAlertService.get).toHaveBeenCalled();
  });

  it('Should call alertService.clear on destroy', () => {
    // WHEN
    comp.ngOnDestroy();

    // THEN
    expect(mockAlertService.clear).toHaveBeenCalled();
  });
});
