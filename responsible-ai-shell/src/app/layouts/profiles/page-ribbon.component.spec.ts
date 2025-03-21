/**  MIT license https://opensource.org/licenses/MIT
”Copyright 2024-2025 Infosys Ltd.”
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/ 
import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { of } from 'rxjs';

import { ProfileInfo } from 'app/layouts/profiles/profile-info.model';
import { ProfileService } from 'app/layouts/profiles/profile.service';

import { PageRibbonComponent } from './page-ribbon.component';

describe('Page Ribbon Component', () => {
  let comp: PageRibbonComponent;
  let fixture: ComponentFixture<PageRibbonComponent>;
  let profileService: ProfileService;

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      declarations: [PageRibbonComponent],
    })
      .overrideTemplate(PageRibbonComponent, '')
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(PageRibbonComponent);
    comp = fixture.componentInstance;
    profileService = TestBed.inject(ProfileService);
  });

  it('Should call profileService.getProfileInfo on init', () => {
    // GIVEN
    jest.spyOn(profileService, 'getProfileInfo').mockReturnValue(of(new ProfileInfo()));

    // WHEN
    comp.ngOnInit();

    // THEN
    expect(profileService.getProfileInfo).toHaveBeenCalled();
  });
});
