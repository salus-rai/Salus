/**  MIT license https://opensource.org/licenses/MIT
”Copyright 2024-2025 Infosys Ltd.”
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/ 
import { waitForAsync, ComponentFixture, TestBed } from '@angular/core/testing';

import { ItemCountComponent } from './item-count.component';

describe('ItemCountComponent test', () => {
  let comp: ItemCountComponent;
  let fixture: ComponentFixture<ItemCountComponent>;

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      declarations: [ItemCountComponent],
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ItemCountComponent);
    comp = fixture.componentInstance;
  });

  describe('UI logic tests', () => {
    it('should initialize with undefined', () => {
      expect(comp.first).toBeUndefined();
      expect(comp.second).toBeUndefined();
      expect(comp.total).toBeUndefined();
    });

    it('should set calculated numbers to undefined if the page value is not yet defined', () => {
      // GIVEN
      comp.params = { page: undefined, totalItems: 0, itemsPerPage: 10 };

      // THEN
      expect(comp.first).toBeUndefined();
      expect(comp.second).toBeUndefined();
    });

    it('should change the content on page change', () => {
      // GIVEN
      comp.params = { page: 1, totalItems: 100, itemsPerPage: 10 };

      // THEN
      expect(comp.first).toBe(1);
      expect(comp.second).toBe(10);
      expect(comp.total).toBe(100);

      // GIVEN
      comp.params = { page: 2, totalItems: 100, itemsPerPage: 10 };

      // THEN
      expect(comp.first).toBe(11);
      expect(comp.second).toBe(20);
      expect(comp.total).toBe(100);
    });

    it('should set the second number to totalItems if this is the last page which contains less than itemsPerPage items', () => {
      // GIVEN
      comp.params = { page: 2, totalItems: 16, itemsPerPage: 10 };

      // THEN
      expect(comp.first).toBe(11);
      expect(comp.second).toBe(16);
      expect(comp.total).toBe(16);
    });
  });
});
