/**
SPDX-License-Identifier: MIT
Copyright 2024 - 2025 Infosys Ltd.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/

import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { of } from 'rxjs';

import { ConfigurationComponent } from './configuration.component';
import { ConfigurationService } from './configuration.service';
import { Bean, PropertySource } from './configuration.model';

describe('ConfigurationComponent', () => {
  let comp: ConfigurationComponent;
  let fixture: ComponentFixture<ConfigurationComponent>;
  let service: ConfigurationService;

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      declarations: [ConfigurationComponent],
      providers: [ConfigurationService],
    })
      .overrideTemplate(ConfigurationComponent, '')
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ConfigurationComponent);
    comp = fixture.componentInstance;
    service = TestBed.inject(ConfigurationService);
  });

  describe('OnInit', () => {
    it('Should call load all on init', () => {
      // GIVEN
      const beans: Bean[] = [
        {
          prefix: 'jhipster',
          properties: {
            clientApp: {
              name: 'jhipsterApp',
            },
          },
        },
      ];
      const propertySources: PropertySource[] = [
        {
          name: 'server.ports',
          properties: {
            'local.server.port': {
              value: '8080',
            },
          },
        },
      ];
      jest.spyOn(service, 'getBeans').mockReturnValue(of(beans));
      jest.spyOn(service, 'getPropertySources').mockReturnValue(of(propertySources));

      // WHEN
      comp.ngOnInit();

      // THEN
      expect(service.getBeans).toHaveBeenCalled();
      expect(service.getPropertySources).toHaveBeenCalled();
      expect(comp.allBeans).toEqual(beans);
      expect(comp.beans).toEqual(beans);
      expect(comp.propertySources).toEqual(propertySources);
    });
  });
});