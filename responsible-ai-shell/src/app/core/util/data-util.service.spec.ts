/**  MIT license https://opensource.org/licenses/MIT
”Copyright 2024-2025 Infosys Ltd.”
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/ 
import { TestBed } from '@angular/core/testing';

import { DataUtils } from './data-util.service';

describe('Data Utils Service Test', () => {
  let service: DataUtils;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [DataUtils],
    });
    service = TestBed.inject(DataUtils);
  });

  describe('byteSize', () => {
    it('should return the bytesize of the text', () => {
      expect(service.byteSize('Hello JHipster')).toBe(`10.5 bytes`);
    });
  });

  describe('openFile', () => {
    it('should open the file in the new window', () => {
      const newWindow = { ...window };
      newWindow.document.write = jest.fn();
      window.open = jest.fn(() => newWindow);
      window.URL.createObjectURL = jest.fn();
      // 'JHipster' in base64 is 'SkhpcHN0ZXI='
      const data = 'SkhpcHN0ZXI=';
      const contentType = 'text/plain';
      service.openFile(data, contentType);
      expect(window.open).toHaveBeenCalledTimes(1);
    });
  });
});
