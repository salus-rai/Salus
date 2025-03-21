/**  MIT license https://opensource.org/licenses/MIT
”Copyright 2024-2025 Infosys Ltd.”
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/ 
import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';

import { HealthModalComponent } from './health-modal.component';

describe('HealthModalComponent', () => {
  let comp: HealthModalComponent;
  let fixture: ComponentFixture<HealthModalComponent>;
  let mockActiveModal: NgbActiveModal;

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      declarations: [HealthModalComponent],
      providers: [NgbActiveModal],
    })
      .overrideTemplate(HealthModalComponent, '')
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(HealthModalComponent);
    comp = fixture.componentInstance;
    mockActiveModal = TestBed.inject(NgbActiveModal);
  });

  describe('readableValue', () => {
    it('should return stringify value', () => {
      // GIVEN
      comp.health = undefined;

      // WHEN
      const result = comp.readableValue({ name: 'jhipster' });

      // THEN
      expect(result).toEqual('{"name":"jhipster"}');
    });

    it('should return string value', () => {
      // GIVEN
      comp.health = undefined;

      // WHEN
      const result = comp.readableValue('jhipster');

      // THEN
      expect(result).toEqual('jhipster');
    });

    it('should return storage space in an human readable unit (GB)', () => {
      // GIVEN
      comp.health = {
        key: 'diskSpace',
        value: {
          status: 'UP',
        },
      };

      // WHEN
      const result = comp.readableValue(1073741825);

      // THEN
      expect(result).toEqual('1.00 GB');
    });

    it('should return storage space in an human readable unit (MB)', () => {
      // GIVEN
      comp.health = {
        key: 'diskSpace',
        value: {
          status: 'UP',
        },
      };

      // WHEN
      const result = comp.readableValue(1073741824);

      // THEN
      expect(result).toEqual('1024.00 MB');
    });

    it('should return string value', () => {
      // GIVEN
      comp.health = {
        key: 'mail',
        value: {
          status: 'UP',
        },
      };

      // WHEN
      const result = comp.readableValue(1234);

      // THEN
      expect(result).toEqual('1234');
    });
  });

  describe('dismiss', () => {
    it('should call dismiss when dismiss modal is called', () => {
      // GIVEN
      const spy = jest.spyOn(mockActiveModal, 'dismiss');

      // WHEN
      comp.dismiss();

      // THEN
      expect(spy).toHaveBeenCalled();
    });
  });
});
