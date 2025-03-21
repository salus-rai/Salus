/**  MIT license https://opensource.org/licenses/MIT
”Copyright 2024-2025 Infosys Ltd.”
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/ 
import { Directive, HostBinding, HostListener, Input } from '@angular/core';
import { DomSanitizer, SafeStyle } from '@angular/platform-browser';

@Directive({
  selector: '[appImageSelect]',
})
export class ImageSelectDirective {
  @Input() toggle: any = false;
  @Input() color: string = 'rgba(134,38,195,0.3)';

  constructor(private doms: DomSanitizer) {}

  @HostBinding('style') get myStyle(): SafeStyle {
    const style: string =
      this.toggle === true
        ? ` border:3px solid #8626C3;
    background: ${this.color}`
        : 'border: none';
    return this.doms.bypassSecurityTrustStyle(style);
  }

  @HostListener('click') onClick() {
    this.toggle = !this.toggle;
    // this.toggle=false;
    // this.resetForm()

    // this.toggle=true;
    setTimeout(() => {
      this.toggle = false;
    }, 7000);
    // this.toggle=false
  }

  resetForm() {
    this.color;
    this.toggle = undefined;
    console.log('hello');
  }
}
