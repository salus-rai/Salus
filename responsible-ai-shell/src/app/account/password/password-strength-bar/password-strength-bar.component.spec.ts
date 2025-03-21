/**  MIT license https://opensource.org/licenses/MIT
”Copyright 2024-2025 Infosys Ltd.”
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/ 
import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';

import { PasswordStrengthBarComponent } from './password-strength-bar.component';

describe('PasswordStrengthBarComponent', () => {
  let comp: PasswordStrengthBarComponent;
  let fixture: ComponentFixture<PasswordStrengthBarComponent>;

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      declarations: [PasswordStrengthBarComponent],
    })
      .overrideTemplate(PasswordStrengthBarComponent, '')
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(PasswordStrengthBarComponent);
    comp = fixture.componentInstance;
  });

  describe('PasswordStrengthBarComponents', () => {
    it('should initialize with default values', () => {
      expect(comp.measureStrength('')).toBe(0);
      expect(comp.colors).toEqual(['#F00', '#F90', '#FF0', '#9F0', '#0F0']);
      expect(comp.getColor(0).idx).toBe(1);
      expect(comp.getColor(0).color).toBe(comp.colors[0]);
    });

    it('should increase strength upon password value change', () => {
      expect(comp.measureStrength('')).toBe(0);
      expect(comp.measureStrength('aa')).toBeGreaterThanOrEqual(comp.measureStrength(''));
      expect(comp.measureStrength('aa^6')).toBeGreaterThanOrEqual(comp.measureStrength('aa'));
      expect(comp.measureStrength('Aa090(**)')).toBeGreaterThanOrEqual(comp.measureStrength('aa^6'));
      expect(comp.measureStrength('Aa090(**)+-07365')).toBeGreaterThanOrEqual(comp.measureStrength('Aa090(**)'));
    });

    it('should change the color based on strength', () => {
      expect(comp.getColor(0).color).toBe(comp.colors[0]);
      expect(comp.getColor(11).color).toBe(comp.colors[1]);
      expect(comp.getColor(22).color).toBe(comp.colors[2]);
      expect(comp.getColor(33).color).toBe(comp.colors[3]);
      expect(comp.getColor(44).color).toBe(comp.colors[4]);
    });
  });
});
