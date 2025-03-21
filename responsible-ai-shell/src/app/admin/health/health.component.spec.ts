/**  MIT license https://opensource.org/licenses/MIT
”Copyright 2024-2025 Infosys Ltd.”
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/ 
import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';
import { HttpErrorResponse } from '@angular/common/http';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { of, throwError } from 'rxjs';

import { HealthComponent } from './health.component';
import { HealthService } from './health.service';
import { Health } from './health.model';

describe('HealthComponent', () => {
  let comp: HealthComponent;
  let fixture: ComponentFixture<HealthComponent>;
  let service: HealthService;

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      declarations: [HealthComponent],
    })
      .overrideTemplate(HealthComponent, '')
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(HealthComponent);
    comp = fixture.componentInstance;
    service = TestBed.inject(HealthService);
  });

  describe('getBadgeClass', () => {
    it('should get badge class', () => {
      const upBadgeClass = comp.getBadgeClass('UP');
      const downBadgeClass = comp.getBadgeClass('DOWN');
      expect(upBadgeClass).toEqual('badge-success');
      expect(downBadgeClass).toEqual('badge-danger');
    });
  });

  describe('refresh', () => {
    it('should call refresh on init', () => {
      // GIVEN
      const health: Health = { status: 'UP', components: { mail: { status: 'UP', details: { mailDetail: 'mail' } } } };
      jest.spyOn(service, 'checkHealth').mockReturnValue(of(health));

      // WHEN
      comp.ngOnInit();

      // THEN
      expect(service.checkHealth).toHaveBeenCalled();
      expect(comp.health).toEqual(health);
    });

    it('should handle a 503 on refreshing health data', () => {
      // GIVEN
      const health: Health = { status: 'DOWN', components: { mail: { status: 'DOWN' } } };
      jest.spyOn(service, 'checkHealth').mockReturnValue(throwError(new HttpErrorResponse({ status: 503, error: health })));

      // WHEN
      comp.refresh();

      // THEN
      expect(service.checkHealth).toHaveBeenCalled();
      expect(comp.health).toEqual(health);
    });
  });
});
