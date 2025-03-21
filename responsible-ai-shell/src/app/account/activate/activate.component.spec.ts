/**  MIT license https://opensource.org/licenses/MIT
”Copyright 2024-2025 Infosys Ltd.”
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/ 
import { TestBed, waitForAsync, tick, fakeAsync, inject } from '@angular/core/testing';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { ActivatedRoute } from '@angular/router';
import { of, throwError } from 'rxjs';

import { ActivateService } from './activate.service';
import { ActivateComponent } from './activate.component';

describe('ActivateComponent', () => {
  let comp: ActivateComponent;

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      declarations: [ActivateComponent],
      providers: [
        {
          provide: ActivatedRoute,
          useValue: { queryParams: of({ key: 'ABC123' }) },
        },
      ],
    })
      .overrideTemplate(ActivateComponent, '')
      .compileComponents();
  }));

  beforeEach(() => {
    const fixture = TestBed.createComponent(ActivateComponent);
    comp = fixture.componentInstance;
  });

  it('calls activate.get with the key from params', inject(
    [ActivateService],
    fakeAsync((service: ActivateService) => {
      jest.spyOn(service, 'get').mockReturnValue(of());

      comp.ngOnInit();
      tick();

      expect(service.get).toHaveBeenCalledWith('ABC123');
    })
  ));

  it('should set set success to true upon successful activation', inject(
    [ActivateService],
    fakeAsync((service: ActivateService) => {
      jest.spyOn(service, 'get').mockReturnValue(of({}));

      comp.ngOnInit();
      tick();

      expect(comp.error).toBe(false);
      expect(comp.success).toBe(true);
    })
  ));

  it('should set set error to true upon activation failure', inject(
    [ActivateService],
    fakeAsync((service: ActivateService) => {
      jest.spyOn(service, 'get').mockReturnValue(throwError('ERROR'));

      comp.ngOnInit();
      tick();

      expect(comp.error).toBe(true);
      expect(comp.success).toBe(false);
    })
  ));
});
