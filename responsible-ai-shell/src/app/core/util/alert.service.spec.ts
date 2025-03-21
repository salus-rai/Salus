/**  MIT license https://opensource.org/licenses/MIT
”Copyright 2024-2025 Infosys Ltd.”
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/ 
import { inject, TestBed } from '@angular/core/testing';

import { Alert, AlertService } from './alert.service';

describe('Alert service test', () => {
  describe('Alert Service Test', () => {
    let extAlerts: Alert[];

    beforeEach(() => {
      TestBed.configureTestingModule({});
      jest.useFakeTimers();
      extAlerts = [];
    });

    it('should produce a proper alert object and fetch it', inject([AlertService], (service: AlertService) => {
      expect(
        service.addAlert({
          type: 'success',
          message: 'Hello Jhipster',
          timeout: 3000,
          toast: true,
          position: 'top left',
        })
      ).toEqual(
        expect.objectContaining({
          type: 'success',
          message: 'Hello Jhipster',
          id: 0,
          timeout: 3000,
          toast: true,
          position: 'top left',
        } as Alert)
      );

      expect(service.get().length).toBe(1);
      expect(service.get()[0]).toEqual(
        expect.objectContaining({
          type: 'success',
          message: 'Hello Jhipster',
          id: 0,
          timeout: 3000,
          toast: true,
          position: 'top left',
        } as Alert)
      );
    }));

    it('should produce a proper alert object and add it to external alert objects array', inject(
      [AlertService],
      (service: AlertService) => {
        expect(
          service.addAlert(
            {
              type: 'success',
              message: 'Hello Jhipster',
              timeout: 3000,
              toast: true,
              position: 'top left',
            },
            extAlerts
          )
        ).toEqual(
          expect.objectContaining({
            type: 'success',
            message: 'Hello Jhipster',
            id: 0,
            timeout: 3000,
            toast: true,
            position: 'top left',
          } as Alert)
        );

        expect(extAlerts.length).toBe(1);
        expect(extAlerts[0]).toEqual(
          expect.objectContaining({
            type: 'success',
            message: 'Hello Jhipster',
            id: 0,
            timeout: 3000,
            toast: true,
            position: 'top left',
          } as Alert)
        );
      }
    ));

    it('should produce an alert object with correct id', inject([AlertService], (service: AlertService) => {
      service.addAlert({ type: 'info', message: 'Hello Jhipster info' });
      expect(service.addAlert({ type: 'success', message: 'Hello Jhipster success' })).toEqual(
        expect.objectContaining({
          type: 'success',
          message: 'Hello Jhipster success',
          id: 1,
        } as Alert)
      );

      expect(service.get().length).toBe(2);
      expect(service.get()[1]).toEqual(
        expect.objectContaining({
          type: 'success',
          message: 'Hello Jhipster success',
          id: 1,
        } as Alert)
      );
    }));

    it('should close an alert correctly', inject([AlertService], (service: AlertService) => {
      const alert0 = service.addAlert({ type: 'info', message: 'Hello Jhipster info' });
      const alert1 = service.addAlert({ type: 'info', message: 'Hello Jhipster info 2' });
      const alert2 = service.addAlert({ type: 'success', message: 'Hello Jhipster success' });
      expect(alert2).toEqual(
        expect.objectContaining({
          type: 'success',
          message: 'Hello Jhipster success',
          id: 2,
        } as Alert)
      );

      expect(service.get().length).toBe(3);
      alert1.close?.(service.get());
      expect(service.get().length).toBe(2);
      expect(service.get()[1]).not.toEqual(
        expect.objectContaining({
          type: 'info',
          message: 'Hello Jhipster info 2',
          id: 1,
        } as Alert)
      );
      alert2.close?.(service.get());
      expect(service.get().length).toBe(1);
      expect(service.get()[0]).not.toEqual(
        expect.objectContaining({
          type: 'success',
          message: 'Hello Jhipster success',
          id: 2,
        } as Alert)
      );
      alert0.close?.(service.get());
      expect(service.get().length).toBe(0);
    }));

    it('should close an alert on timeout correctly', inject([AlertService], (service: AlertService) => {
      service.addAlert({ type: 'info', message: 'Hello Jhipster info' });

      expect(service.get().length).toBe(1);

      jest.advanceTimersByTime(6000);

      expect(service.get().length).toBe(0);
    }));

    it('should clear alerts', inject([AlertService], (service: AlertService) => {
      service.addAlert({ type: 'info', message: 'Hello Jhipster info' });
      service.addAlert({ type: 'danger', message: 'Hello Jhipster info' });
      service.addAlert({ type: 'success', message: 'Hello Jhipster info' });
      expect(service.get().length).toBe(3);
      service.clear();
      expect(service.get().length).toBe(0);
    }));

    it('should produce a scoped alert', inject([AlertService], (service: AlertService) => {
      expect(
        service.addAlert(
          {
            type: 'success',
            message: 'Hello Jhipster',
            timeout: 3000,
            toast: true,
            position: 'top left',
          },
          []
        )
      ).toEqual(
        expect.objectContaining({
          type: 'success',
          message: 'Hello Jhipster',
          id: 0,
          timeout: 3000,
          toast: true,
          position: 'top left',
        } as Alert)
      );

      expect(service.get().length).toBe(0);
    }));

    it('should produce a success message', inject([AlertService], (service: AlertService) => {
      expect(service.addAlert({ type: 'success', message: 'Hello Jhipster' })).toEqual(
        expect.objectContaining({
          type: 'success',
          message: 'Hello Jhipster',
        } as Alert)
      );
    }));

    it('should produce a success message with custom position', inject([AlertService], (service: AlertService) => {
      expect(service.addAlert({ type: 'success', message: 'Hello Jhipster', position: 'bottom left' })).toEqual(
        expect.objectContaining({
          type: 'success',
          message: 'Hello Jhipster',
          position: 'bottom left',
        } as Alert)
      );
    }));

    it('should produce a error message', inject([AlertService], (service: AlertService) => {
      expect(service.addAlert({ type: 'danger', message: 'Hello Jhipster' })).toEqual(
        expect.objectContaining({
          type: 'danger',
          message: 'Hello Jhipster',
        } as Alert)
      );
    }));

    it('should produce a warning message', inject([AlertService], (service: AlertService) => {
      expect(service.addAlert({ type: 'warning', message: 'Hello Jhipster' })).toEqual(
        expect.objectContaining({
          type: 'warning',
          message: 'Hello Jhipster',
        } as Alert)
      );
    }));

    it('should produce a info message', inject([AlertService], (service: AlertService) => {
      expect(service.addAlert({ type: 'info', message: 'Hello Jhipster' })).toEqual(
        expect.objectContaining({
          type: 'info',
          message: 'Hello Jhipster',
        } as Alert)
      );
    }));
  });
});
