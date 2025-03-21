/**  MIT license https://opensource.org/licenses/MIT
”Copyright 2024-2025 Infosys Ltd.”
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/ 
import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';
import { ActivatedRoute } from '@angular/router';
import { of } from 'rxjs';

import { Authority } from 'app/config/authority.constants';
import { User } from '../user-management.model';

import { UserManagementDetailComponent } from './user-management-detail.component';

describe('User Management Detail Component', () => {
  let comp: UserManagementDetailComponent;
  let fixture: ComponentFixture<UserManagementDetailComponent>;

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      declarations: [UserManagementDetailComponent],
      providers: [
        {
          provide: ActivatedRoute,
          useValue: {
            data: of({ user: new User(123, 'user', 'first', 'last', 'first@last.com', true, 'en', [Authority.USER], 'admin') }),
          },
        },
      ],
    })
      .overrideTemplate(UserManagementDetailComponent, '')
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(UserManagementDetailComponent);
    comp = fixture.componentInstance;
  });

  describe('OnInit', () => {
    it('Should call load all on init', () => {
      // WHEN
      comp.ngOnInit();

      // THEN
      expect(comp.user).toEqual(
        expect.objectContaining({
          id: 123,
          login: 'user',
          firstName: 'first',
          lastName: 'last',
          email: 'first@last.com',
          activated: true,
          langKey: 'en',
          authorities: [Authority.USER],
          createdBy: 'admin',
        })
      );
    });
  });
});
