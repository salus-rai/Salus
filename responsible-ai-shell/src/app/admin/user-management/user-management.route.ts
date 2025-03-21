/**  MIT license https://opensource.org/licenses/MIT
”Copyright 2024-2025 Infosys Ltd.”
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/ 
import { Injectable } from '@angular/core';
import { Resolve, ActivatedRouteSnapshot, Routes } from '@angular/router';
import { Observable, of } from 'rxjs';

import { User, IUser } from './user-management.model';
import { UserManagementService } from './service/user-management.service';
import { UserManagementComponent } from './list/user-management.component';
import { UserManagementDetailComponent } from './detail/user-management-detail.component';
import { UserManagementUpdateComponent } from './update/user-management-update.component';

@Injectable({ providedIn: 'root' })
export class UserManagementResolve implements Resolve<IUser> {
  constructor(private service: UserManagementService) {}

  resolve(route: ActivatedRouteSnapshot): Observable<IUser> {
    const id = route.params['login'];
    if (id) {
      return this.service.find(id);
    }
    return of(new User());
  }
}

export const userManagementRoute: Routes = [
  {
    path: '',
    component: UserManagementComponent,
    data: {
      defaultSort: 'id,asc',
    },
  },
  {
    path: ':login/view',
    component: UserManagementDetailComponent,
    resolve: {
      user: UserManagementResolve,
    },
  },
  {
    path: 'new',
    component: UserManagementUpdateComponent,
    resolve: {
      user: UserManagementResolve,
    },
  },
  {
    path: ':login/edit',
    component: UserManagementUpdateComponent,
    resolve: {
      user: UserManagementResolve,
    },
  },
];
