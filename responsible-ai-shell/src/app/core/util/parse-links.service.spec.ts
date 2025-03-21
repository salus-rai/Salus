/**  MIT license https://opensource.org/licenses/MIT
”Copyright 2024-2025 Infosys Ltd.”
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/ 
import { inject, TestBed } from '@angular/core/testing';

import { ParseLinks } from './parse-links.service';

describe('Parse links service test', () => {
  describe('Parse Links Service Test', () => {
    beforeEach(() => {
      TestBed.configureTestingModule({
        providers: [ParseLinks],
      });
    });

    it('should throw an error when passed an empty string', inject([ParseLinks], (service: ParseLinks) => {
      expect(function () {
        service.parse('');
      }).toThrow(new Error('input must not be of zero length'));
    }));

    it('should throw an error when passed without comma', inject([ParseLinks], (service: ParseLinks) => {
      expect(function () {
        service.parse('test');
      }).toThrow(new Error('section could not be split on ";"'));
    }));

    it('should throw an error when passed without semicolon', inject([ParseLinks], (service: ParseLinks) => {
      expect(function () {
        service.parse('test,test2');
      }).toThrow(new Error('section could not be split on ";"'));
    }));

    it('should return links when headers are passed', inject([ParseLinks], (service: ParseLinks) => {
      const links = { last: 0, first: 0 };
      expect(service.parse(' </api/audits?page=0&size=20>; rel="last",</api/audits?page=0&size=20>; rel="first"')).toEqual(links);
    }));
  });
});
