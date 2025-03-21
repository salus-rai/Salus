/**  MIT license https://opensource.org/licenses/MIT
”Copyright 2024-2025 Infosys Ltd.”
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/ 
import { Component, OnInit } from '@angular/core';

import { ConfigurationService } from './configuration.service';
import { Bean, PropertySource } from './configuration.model';

@Component({
  selector: 'jhi-configuration',
  templateUrl: './configuration.component.html',
})
export class ConfigurationComponent implements OnInit {
  allBeans!: Bean[];
  beans: Bean[] = [];
  beansFilter = '';
  beansAscending = true;
  propertySources: PropertySource[] = [];

  constructor(private configurationService: ConfigurationService) {}

  ngOnInit(): void {
    this.configurationService.getBeans().subscribe(beans => {
      this.allBeans = beans;
      this.filterAndSortBeans();
    });

    this.configurationService.getPropertySources().subscribe(propertySources => (this.propertySources = propertySources));
  }

  filterAndSortBeans(): void {
    const beansAscendingValue = this.beansAscending ? -1 : 1;
    const beansAscendingValueReverse = this.beansAscending ? 1 : -1;
    this.beans = this.allBeans
      .filter(bean => !this.beansFilter || bean.prefix.toLowerCase().includes(this.beansFilter.toLowerCase()))
      .sort((a, b) => (a.prefix < b.prefix ? beansAscendingValue : beansAscendingValueReverse));
  }
}
