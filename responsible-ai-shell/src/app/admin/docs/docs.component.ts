/**  MIT license https://opensource.org/licenses/MIT
”Copyright 2024-2025 Infosys Ltd.”
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/ 
import { Component, OnInit } from '@angular/core';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';
@Component({
  selector: 'jhi-docs',
  templateUrl: './docs.component.html',
  styleUrls: ['./docs.component.scss'],
})
export class DocsComponent implements OnInit {
  public url = '';
  public urlSafe: SafeResourceUrl = '';

  constructor(public sanitizer: DomSanitizer) {}

  ngOnInit(): void {
    let apiUrl = 'https://localhost:8080/';
    apiUrl = apiUrl?.endsWith('/') ? apiUrl.substring(0, apiUrl.length - 1) : apiUrl;
    // eslint-disable-next-line @typescript-eslint/restrict-template-expressions
    this.url = 'production' === 'production' ? `swagger-ui/index.html?apiUrl=${apiUrl}` : 'swagger-ui/index.html';
    this.urlSafe = this.sanitizer.bypassSecurityTrustResourceUrl(this.url);
  }
}
