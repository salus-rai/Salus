/**  MIT license https://opensource.org/licenses/MIT
”Copyright 2024-2025 Infosys Ltd.”
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/ 
jest.mock('app/core/auth/account.service');

import { waitForAsync, ComponentFixture, TestBed } from '@angular/core/testing';
import { Router, RouterEvent, NavigationEnd, NavigationStart } from '@angular/router';
import { Title } from '@angular/platform-browser';
import { Subject, of } from 'rxjs';

import { AccountService } from 'app/core/auth/account.service';

import { MainComponent } from './main.component';

describe('MainComponent', () => {
  let comp: MainComponent;
  let fixture: ComponentFixture<MainComponent>;
  let titleService: Title;
  let mockAccountService: AccountService;
  const routerEventsSubject = new Subject<RouterEvent>();
  const routerState: any = { snapshot: { root: { data: {} } } };
  class MockRouter {
    events = routerEventsSubject;
    routerState = routerState;
  }

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      declarations: [MainComponent],
      providers: [
        Title,
        AccountService,
        {
          provide: Router,
          useClass: MockRouter,
        },
      ],
    })
      .overrideTemplate(MainComponent, '')
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(MainComponent);
    comp = fixture.componentInstance;
    titleService = TestBed.inject(Title);
    mockAccountService = TestBed.inject(AccountService);
    mockAccountService.identity = jest.fn(() => of(null));
    mockAccountService.getAuthenticationState = jest.fn(() => of(null));
  });

  describe('page title', () => {
    const defaultPageTitle = 'Angular JWTFE';
    const parentRoutePageTitle = 'parentTitle';
    const childRoutePageTitle = 'childTitle';
    const navigationEnd = new NavigationEnd(1, '', '');
    const navigationStart = new NavigationStart(1, '');

    beforeEach(() => {
      routerState.snapshot.root = { data: {} };
      jest.spyOn(titleService, 'setTitle');
      comp.ngOnInit();
    });

    describe('navigation end', () => {
      it('should set page title to default title if pageTitle is missing on routes', () => {
        // WHEN
        routerEventsSubject.next(navigationEnd);

        // THEN
        expect(titleService.setTitle).toHaveBeenCalledWith(defaultPageTitle);
      });

      it('should set page title to root route pageTitle if there is no child routes', () => {
        // GIVEN
        routerState.snapshot.root.data = { pageTitle: parentRoutePageTitle };

        // WHEN
        routerEventsSubject.next(navigationEnd);

        // THEN
        expect(titleService.setTitle).toHaveBeenCalledWith(parentRoutePageTitle);
      });

      it('should set page title to child route pageTitle if child routes exist and pageTitle is set for child route', () => {
        // GIVEN
        routerState.snapshot.root.data = { pageTitle: parentRoutePageTitle };
        routerState.snapshot.root.firstChild = { data: { pageTitle: childRoutePageTitle } };

        // WHEN
        routerEventsSubject.next(navigationEnd);

        // THEN
        expect(titleService.setTitle).toHaveBeenCalledWith(childRoutePageTitle);
      });

      it('should set page title to parent route pageTitle if child routes exists but pageTitle is not set for child route data', () => {
        // GIVEN
        routerState.snapshot.root.data = { pageTitle: parentRoutePageTitle };
        routerState.snapshot.root.firstChild = { data: {} };

        // WHEN
        routerEventsSubject.next(navigationEnd);

        // THEN
        expect(titleService.setTitle).toHaveBeenCalledWith(parentRoutePageTitle);
      });
    });

    describe('navigation start', () => {
      it('should not set page title on navigation start', () => {
        // WHEN
        routerEventsSubject.next(navigationStart);

        // THEN
        expect(titleService.setTitle).not.toHaveBeenCalled();
      });
    });
  });
});
